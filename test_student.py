import unittest
from proj3 import *


class TestHuffmanEncoding(unittest.TestCase):
    def test_heapify_up(self):
        heap = MinHeap([Node(5, "a"), Node(10, "b"), Node(1, "c")])
        new_heap = heapify_up(heap, 2)
        self.assertEqual(new_heap.data[0].freq, 1)
        self.assertEqual(new_heap.data[0].char, "c")
        self.assertEqual(len(new_heap.data), 3)

    def test_insert(self):
        heap = MinHeap([Node(3, "a"), Node(5, "b")])
        new_heap = insert(heap, Node(1, "c"))
        self.assertEqual(len(new_heap.data), 3)
        self.assertEqual(new_heap.data[0].freq, 1)
        self.assertEqual(new_heap.data[0].char, "c")

    def test_extract_min(self):
        heap = MinHeap([])
        heap = insert(heap, Node(4, "a"))
        heap = insert(heap, Node(2, "b"))
        heap = insert(heap, Node(7, "c"))
        new_heap, smallest = extract_min(heap)
        self.assertEqual(smallest.freq, 2)
        self.assertEqual(smallest.char, "b")
        self.assertEqual(len(new_heap.data), 2)
        self.assertEqual(new_heap.data[0].freq, 4)

    def test_count_frequency(self):
        freq = count_frequency("hello")
        self.assertEqual(freq["h"], 1)
        self.assertEqual(freq["e"], 1)
        self.assertEqual(freq["l"], 2)
        self.assertEqual(freq["o"], 1)

    def test_create_priority_queue(self):
        freq = {"a": 3, "b": 1, "c": 2}
        heap = create_priority_queue(freq)
        self.assertEqual(len(heap.data), 3)
        self.assertEqual(heap.data[0].freq, 1)

    def test_build_tree(self):
        freq = count_frequency("aab")
        heap = create_priority_queue(freq)
        root = build_tree_from_queue(heap)
        self.assertEqual(root.freq, 3)
        self.assertIsNotNone(root.left)
        self.assertIsNotNone(root.right)

    def test_generate_codes(self):
        freq = count_frequency("aab")
        heap = create_priority_queue(freq)
        root = build_tree_from_queue(heap)
        codes = generate_codes(root)
        self.assertIn("a", codes)
        self.assertIn("b", codes)
        self.assertTrue(len(codes["a"]) > 0)
        self.assertTrue(len(codes["b"]) > 0)

    def test_encode_decode(self):
        text = "hello"
        encoded, decoded, codes = huffman_encoding(text)
        self.assertEqual(decoded, text)
        self.assertTrue(isinstance(encoded, str))
        self.assertTrue(isinstance(codes, dict))

    def test_single_character(self):
        text = "aaaaa"
        encoded, decoded, codes = huffman_encoding(text)
        self.assertEqual(decoded, text)
        self.assertEqual(codes["a"], "0")
        self.assertEqual(encoded, "00000")

    def test_repeated_characters(self):
        text = "aaabbc"
        encoded, decoded, codes = huffman_encoding(text)
        self.assertEqual(decoded, text)
        self.assertEqual(len(codes), 3)

    def test_empty_string(self):
        encoded, decoded, codes = huffman_encoding("")
        self.assertEqual(encoded, "")
        self.assertEqual(decoded, "")
        self.assertEqual(codes, {})

if __name__ == "__main__":
    unittest.main()