"""Transform functional tests."""

import unittest
import os
import os.path
import shutil
import numpy as np

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')


class GeneralPurposeTransoformTests(unittest.TestCase):

    def setUp(self):
        from jicbioimage.core.io import AutoName
        AutoName.count = 0
        AutoName.directory = TMP_DIR
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        from jicbioimage.core.io import AutoName
        AutoName.count = 0
        shutil.rmtree(TMP_DIR)

    def test_max_intensity_projection(self):
        from jicbioimage.transform import max_intensity_projection
        from jicbioimage.core.image import Image
        slice0 = np.array(
            [[0, 1, 2],
             [0, 1, 2],
             [0, 1, 2]], dtype=np.uint8)
        slice1 = np.array(
            [[2, 1, 0],
             [2, 1, 0],
             [2, 1, 0]], dtype=np.uint8)
        expected = np.array(
            [[2, 1, 2],
             [2, 1, 2],
             [2, 1, 2]], dtype=np.uint8)
        stack = np.dstack([slice0, slice1])
        max_projection = max_intensity_projection(stack)
        self.assertTrue(np.array_equal(expected, max_projection))
        self.assertTrue(isinstance(max_projection, Image))

    def test_min_intensity_projection(self):
        from jicbioimage.transform import min_intensity_projection
        from jicbioimage.core.image import Image
        slice0 = np.array(
            [[0, 1, 2],
             [0, 1, 2],
             [0, 1, 2]], dtype=np.uint8)
        slice1 = np.array(
            [[2, 1, 0],
             [2, 1, 0],
             [2, 1, 0]], dtype=np.uint8)
        expected = np.array(
            [[0, 1, 0],
             [0, 1, 0],
             [0, 1, 0]], dtype=np.uint8)
        stack = np.dstack([slice0, slice1])
        min_projection = min_intensity_projection(stack)
        self.assertTrue(np.array_equal(expected, min_projection))
        self.assertTrue(isinstance(min_projection, Image))

    def test_mean_intensity_projection_uint8(self):
        from jicbioimage.transform import mean_intensity_projection
        from jicbioimage.core.image import Image
        slice0 = np.array(
            [[0, 0, 0],
             [1, 1, 1],
             [2, 2, 2]], dtype=np.uint8)
        slice1 = np.array(
            [[0, 1, 2],
             [0, 1, 2],
             [0, 1, 2]], dtype=np.uint8)
        stack = np.dstack([slice0, slice1])
        expected = np.array(
            [[0, 0, 1],
             [0, 1, 1],
             [1, 1, 2]], dtype=np.uint8)
        mean_projection = mean_intensity_projection(stack)
        self.assertTrue(np.array_equal(expected, mean_projection))
        self.assertTrue(isinstance(mean_projection, Image))

    def test_mean_intensity_projection_float(self):
        from jicbioimage.transform import mean_intensity_projection
        from jicbioimage.core.image import Image
        slice0 = np.array(
            [[0, 0, 0],
             [1, 1, 1],
             [2, 2, 2]], dtype=np.float)
        slice1 = np.array(
            [[0, 1, 2],
             [0, 1, 2],
             [0, 1, 2]], dtype=np.float)
        stack = np.dstack([slice0, slice1])
        expected = np.mean(stack, axis=2)
        mean_projection = mean_intensity_projection(stack)
        self.assertTrue(np.array_equal(expected, mean_projection))
        self.assertTrue(isinstance(mean_projection, Image))

    def test_median_intensity_projection_uint8(self):
        from jicbioimage.transform import median_intensity_projection
        from jicbioimage.core.image import Image
        slice0 = np.array(
            [[0, 0, 0],
             [1, 1, 1],
             [2, 2, 2]], dtype=np.uint8)
        slice1 = np.array(
            [[0, 0, 0],
             [1, 1, 1],
             [2, 2, 2]], dtype=np.uint8)
        slice2 = np.array(
            [[0, 1, 2],
             [0, 1, 2],
             [0, 1, 2]], dtype=np.uint8)
        stack = np.dstack([slice0, slice1, slice2])
        expected = np.array(
            [[0, 0, 0],
             [1, 1, 1],
             [2, 2, 2]], dtype=np.uint8)
        median_projection = median_intensity_projection(stack)
        self.assertTrue(np.array_equal(expected, median_projection))
        self.assertTrue(isinstance(median_projection, Image))

    def test_smooth_gaussian(self):
        from jicbioimage.transform import smooth_gaussian
        from jicbioimage.core.image import Image
        array = np.array(
            [[0., 0., 0.],
             [0., 1., 0.],
             [0., 0., 0.]], dtype=np.float)
        expected = np.array(
            [[0.05855018, 0.09653293, 0.05855018],
             [0.09653293, 0.15915589, 0.09653293],
             [0.05855018, 0.09653293, 0.05855018]], dtype=np.float)
        smoothed = smooth_gaussian(array)
        self.assertTrue(np.allclose(expected, smoothed))
        self.assertTrue(isinstance(smoothed, Image))

        # The smooth_gaussian function only makes sense on dtype np.float.
        with self.assertRaises(TypeError):
            smoothed = smooth_gaussian(array.astype(np.uint8))

    def test_threshold_otsu(self):
        from jicbioimage.transform import threshold_otsu
        from jicbioimage.core.image import Image

        # Test with uint8.
        array = np.array(
            [[1,  2,  3],
             [7,  8,  9]], dtype=np.uint8)
        expected = np.array(
            [[0,  0,  0],
             [1,  1,  1]], dtype=np.bool)
        thresholded = threshold_otsu(array)
        self.assertTrue(np.array_equal(expected, thresholded))
        self.assertTrue(isinstance(thresholded, Image))

        # Test with float.
        array = np.array(
            [[1,  2,  3],
             [7,  8,  9]], dtype=np.float)
        expected = np.array(
            [[0,  0,  0],
             [1,  1,  1]], dtype=np.bool)
        thresholded = threshold_otsu(array)
        self.assertTrue(np.array_equal(expected, thresholded))
        self.assertTrue(isinstance(thresholded, Image))

    def test_threshold_otsu_multiplier(self):
        from jicbioimage.transform import threshold_otsu
        array = np.array(
            [[1,  2,  3],
             [7,  8,  9]], dtype=np.uint8)
        # Threshold used: 3 * 0.6 = 1.79
        expected = np.array(
            [[0,  1,  1],
             [1,  1,  1]], dtype=np.bool)
        thresholded = threshold_otsu(array, multiplier=0.6)
        self.assertTrue(np.array_equal(expected, thresholded))

    def test_remove_small_objects(self):
        from jicbioimage.transform import remove_small_objects
        from jicbioimage.core.image import Image
        array = np.array(
            [[0,  0,  0, 0, 1],
             [0,  1,  1, 0, 0],
             [0,  1,  1, 0, 0],
             [0,  0,  0, 1, 0],
             [1,  1,  0, 1, 0]], dtype=np.bool)
        expected_con1 = np.array(
            [[0,  0,  0, 0, 0],
             [0,  1,  1, 0, 0],
             [0,  1,  1, 0, 0],
             [0,  0,  0, 0, 0],
             [0,  0,  0, 0, 0]], dtype=np.bool)
        no_small = remove_small_objects(array, min_size=4)
        self.assertTrue(np.array_equal(expected_con1, no_small))
        self.assertTrue(isinstance(no_small, Image))

        expected_con2 = np.array(
            [[0,  0,  0, 0, 0],
             [0,  1,  1, 0, 0],
             [0,  1,  1, 0, 0],
             [0,  0,  0, 1, 0],
             [0,  0,  0, 1, 0]], dtype=np.bool)
        no_small = remove_small_objects(array, min_size=4, connectivity=2)
        self.assertTrue(np.array_equal(expected_con2, no_small))

        # The remove_small_objects function only makes sense on dtype np.bool.
        with self.assertRaises(TypeError):
            remove_small_objects(array.astype(np.uint8))

    def test_invert_bool(self):
        from jicbioimage.transform import invert
        from jicbioimage.core.image import Image
        array = np.array(
            [[1,  1,  1],
             [0,  0,  0]], dtype=np.bool)
        expected = np.array(
            [[0,  0,  0],
             [1,  1,  1]], dtype=np.bool)
        inverted = invert(array)
        self.assertTrue(np.array_equal(expected, inverted))
        self.assertTrue(isinstance(inverted, Image))

    def test_invert_uint8(self):
        from jicbioimage.transform import invert
        from jicbioimage.core.image import Image
        array = np.array(
            [[1,  1,  1],
             [0,  0,  0]], dtype=np.uint8)
        expected = np.array(
            [[254,  254,  254],
             [255,  255,  255]], dtype=np.uint8)
        inverted = invert(array)
        self.assertTrue(np.array_equal(expected, inverted))
        self.assertTrue(isinstance(inverted, Image))

    def test_dilate_binary(self):
        from jicbioimage.transform import dilate_binary
        from jicbioimage.core.image import Image
        array = np.array(
            [[0,  0,  0, 0, 0],
             [0,  0,  0, 0, 0],
             [0,  0,  1, 0, 0],
             [0,  0,  0, 0, 0],
             [0,  0,  0, 0, 0]], dtype=np.bool)
        expected = np.array(
            [[0,  0,  0, 0, 0],
             [0,  0,  1, 0, 0],
             [0,  1,  1, 1, 0],
             [0,  0,  1, 0, 0],
             [0,  0,  0, 0, 0]], dtype=np.bool)
        dilated = dilate_binary(array)
        self.assertTrue(np.array_equal(expected, dilated))
        self.assertTrue(isinstance(dilated, Image))

        # The dilate_binary function only makes sense on dtype bool.
        with self.assertRaises(TypeError):
            dilate_binary(array.astype(np.uint8))

    def test_dilate_binary_with_selem(self):
        from jicbioimage.transform import dilate_binary
        selem = np.ones((3, 3))
        array = np.array(
            [[0,  0,  0, 0, 0],
             [0,  0,  0, 0, 0],
             [0,  0,  1, 0, 0],
             [0,  0,  0, 0, 0],
             [0,  0,  0, 0, 0]], dtype=np.bool)
        expected = np.array(
            [[0,  0,  0, 0, 0],
             [0,  1,  1, 1, 0],
             [0,  1,  1, 1, 0],
             [0,  1,  1, 1, 0],
             [0,  0,  0, 0, 0]], dtype=np.bool)
        dilated = dilate_binary(array, selem=selem)
        self.assertTrue(np.array_equal(expected, dilated))

    def test_erode_binary(self):
        from jicbioimage.transform import erode_binary
        from jicbioimage.core.image import Image
        array = np.array(
            [[0,  0,  0, 0, 0],
             [0,  0,  1, 0, 0],
             [0,  1,  1, 1, 0],
             [0,  0,  1, 0, 0],
             [0,  0,  0, 0, 0]], dtype=np.bool)
        expected = np.array(
            [[0,  0,  0, 0, 0],
             [0,  0,  0, 0, 0],
             [0,  0,  1, 0, 0],
             [0,  0,  0, 0, 0],
             [0,  0,  0, 0, 0]], dtype=np.bool)
        eroded = erode_binary(array)
        self.assertTrue(np.array_equal(expected, eroded))
        self.assertTrue(isinstance(eroded, Image))

        # The erode_binary function only makes sense on dtype bool.
        with self.assertRaises(TypeError):
            erode_binary(array.astype(np.uint8))

    def test_erode_binary_with_selem(self):
        from jicbioimage.transform import erode_binary
        selem = np.ones((3, 3))
        array = np.array(
            [[0,  0,  0, 0,  0, 0, 0],
             [0,  1,  0, 1,  1, 1, 0],
             [0,  1,  1, 1,  1, 1, 0],
             [0,  1,  1, 1,  1, 1, 0],
             [0,  1,  1, 1,  1, 1, 0],
             [0,  1,  1, 1,  1, 1, 0],
             [0,  0,  0, 0,  0, 0, 0]], dtype=np.bool)
        expected = np.array(
            [[0,  0,  0, 0,  0, 0, 0],
             [0,  0,  0, 0,  0, 0, 0],
             [0,  0,  0, 0,  1, 0, 0],
             [0,  0,  1, 1,  1, 0, 0],
             [0,  0,  1, 1,  1, 0, 0],
             [0,  0,  0, 0,  0, 0, 0],
             [0,  0,  0, 0,  0, 0, 0]], dtype=np.bool)
        eroded = erode_binary(array, selem=selem)
        self.assertTrue(np.array_equal(expected, eroded))

    def test_find_edges_sobel(self):
        from jicbioimage.transform import find_edges_sobel
        from jicbioimage.core.image import Image
        array = np.array(
            [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 255, 255, 255, 0, 0],
             [0, 0, 255, 255, 255, 0, 0],
             [0, 0, 255, 255, 255, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]], dtype=np.uint8)
        expected = np.array(
            [[0, 0, 0, 0, 0, 0, 0],
             [0, 0.25, 0.55901699, 0.70710678, 0.55901699, 0.25, 0],
             [0, 0.55901699, 0.75, 0.70710678, 0.75, 0.55901699, 0],
             [0, 0.70710678, 0.70710678,    0, 0.70710678, 0.70710678, 0],
             [0, 0.55901699, 0.75, 0.70710678, 0.75, 0.55901699, 0],
             [0, 0.25, 0.55901699, 0.70710678, 0.55901699, 0.25, 0],
             [0, 0, 0, 0, 0, 0, 0]], dtype=np.float)
        edges = find_edges_sobel(array)
        self.assertTrue(np.allclose(expected, edges))
        self.assertTrue(isinstance(edges, Image))

    def test_find_edges_sobel_with_mask(self):
        from jicbioimage.transform import find_edges_sobel
        mask = np.array(
            [[1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 0, 0, 0],
             [1, 1, 1, 1, 0, 0, 0],
             [1, 1, 1, 1, 0, 0, 0]], dtype=np.uint8)
        array = np.array(
            [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 255, 255, 255, 0, 0],
             [0, 0, 255, 255, 255, 0, 0],
             [0, 0, 255, 255, 255, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]], dtype=np.uint8)
        expected = np.array(
            [[0, 0, 0, 0, 0, 0, 0],
             [0, 0.25, 0.55901699, 0.70710678, 0.55901699, 0.25, 0],
             [0, 0.55901699, 0.75, 0.70710678, 0.75, 0.55901699, 0],
             [0, 0.70710678, 0.70710678,    0, 0, 0, 0],
             [0, 0.55901699, 0.75, 0, 0, 0, 0],
             [0, 0.25, 0.55901699, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]], dtype=np.float)
        edges = find_edges_sobel(array, mask=mask)
        self.assertTrue(np.allclose(expected, edges))

if __name__ == '__main__':
    unittest.main()
