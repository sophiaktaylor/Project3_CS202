from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Node:
    freq: int
    char: str
    left: Node | None = None
    right: Node | None  = None

    def __str__(self):
        return f"Node: {self.char}, Freq: {self.freq}"


@dataclass(frozen=True)
class MinHeap:
    data: list[Node] = field(default_factory=list)


def heapify_up(heap: MinHeap, index: int) -> MinHeap:
    if index <= 0:
        return heap
    parent = (index - 1) // 2
    if heap.data[index] < heap.data[parent]:
        new_data = heap.data[:]
        new_data[index], new_data[parent] = new_data[parent], new_data[index]
        return heapify_up(MinHeap(new_data), parent)
    return heap


def insert(heap: MinHeap, element: Node) -> MinHeap:
    new_data = heap.data + [element]
    new_heap = MinHeap(new_data)
    return heapify_up(new_heap, len(new_data) - 1)


def heapify_down(heap: MinHeap, index: int) -> MinHeap:
    left = 2 * index + 1
    right = 2 * index + 2
    smallest = index
    if left < len(heap.data) and heap.data[left] < heap.data[smallest]:
        smallest = left
    if right < len(heap.data) and heap.data[right] < heap.data[smallest]:
        smallest = right
    if smallest != index:
        new_data = heap.data[:]
        new_data[index], new_data[smallest] = new_data[smallest], new_data[index]
        return heapify_down(MinHeap(new_data), smallest)
    return heap


def extract_min(heap: MinHeap) -> tuple[MinHeap, Node]:
    if len(heap.data) == 0:
        raise IndexError("Empty heap")
    if len(heap.data) == 1:
        return MinHeap([]), heap.data[0]
    minimum = heap.data[0]
    last = heap.data[-1]
    new_data = [last] + heap.data[1:-1]
    new_heap = heapify_down(MinHeap(new_data), 0)
    return new_heap, minimum

      
def count_frequency(s: str)-> dict[str,int]:
    frequency = {}
    for char in s:
        if char in frequency:
            frequency[char] = frequency[char] + 1
        else:
            frequency[char] = 1
    return frequency


def create_priority_queue(frequency: dict[str, int]) -> MinHeap:
    heap = MinHeap([])
    for char in frequency:
        node = Node(frequency[char], char)
        heap = insert(heap, node)
    return heap


def build_tree_from_queue(priority_queue: MinHeap) -> Node:
    heap = priority_queue
    if len(heap.data) == 0:
        return None
    while len(heap.data) > 1:
        heap, first = extract_min(heap)
        heap, second = extract_min(heap)
        new_node = Node(first.freq + second.freq, first.char + second.char, first, second)
        heap = insert(heap, new_node)
    return heap.data[0]


def generate_codes(node: Node | None, prefix="", code: dict | None =None)-> dict:
    if code is None:
        code = {}  
    if node is None:
        return code
    if node.left is None and node.right is None:
        if prefix == "":
            code[node.char] = "0"
        else:
            code[node.char] = prefix
        return code
    generate_codes(node.left, prefix + "0", code)
    generate_codes(node.right, prefix + "1", code)
    return code


def encode(s: str, codes: dict)-> str:
    result = ""
    for char in s:
        result = result + codes[char]
    return result


def decode(encoded_string: str, root: Node):
    if root is None:
        return ""
    if root.left is None and root.right is None:
        return root.char * len(encoded_string)
    result = ""
    current = root
    for bit in encoded_string:
        if bit == "0":
            current = current.left
        else:
            current = current.right
        if current.left is None and current.right is None:
            result = result + current.char
            current = root
    return result


def huffman_encoding(s:str):
    #Do Not Change this function
    frequency = count_frequency(s)
    pq = create_priority_queue(frequency)
    root = build_tree_from_queue(pq)
    codes = generate_codes(root)
    encoded_string = encode(s, codes)
    decoded_string = decode(encoded_string,root)
    return encoded_string, decoded_string, codes