from PIL import Image
from numba import njit
import numpy as np
import math


@njit
def create_mandelbrot_matrix(height, width, min_re=-2.0, max_re=1.0, min_im=-1.2, max_iterations=50):
    matrix = []

    max_im = min_im + (max_re - min_re) * height / width

    re_factor = (max_re - min_re) / (width - 1)
    im_factor = (max_im - min_im) / (height - 1)

    for y in range(height):
        c_im = max_im - y * im_factor
        for x in range(width):
            c_re = min_re + x * re_factor

            z_re, z_im = c_re, c_im
            is_inside = True

            for n in range(max_iterations):
                z_re2, z_im2 = z_re * z_re, z_im * z_im
                if z_re2 + z_im2 > 4:
                    is_inside = False
                    factor = math.sqrt(n / max_iterations)
                    intensity = round(255 * factor)
                    matrix.append((intensity, intensity, intensity))
                    break
                z_im = 2 * z_re * z_im + c_im
                z_re = z_re2 - z_im2 + c_re
            if is_inside:
                matrix.append((0, 0, 0))
    return matrix


def create_image_from_matrix(height, width, matrix):
    image = Image.new('RGB', (height, width))
    image.putdata(matrix)
    return image


@njit
def find_distance_between_two_points(start, end):
    if start < end:
        distance = abs(end - start)
    else:
        distance = -(abs(start - end))
    return distance


def create_mandelbrot_gif_frames(frames_number, height, width, min_re, max_re, min_im):
    frames = list()
    min_re_range = np.arange(-2.0, min_re, find_distance_between_two_points(-2, min_re) / frames_number)
    max_re_range = np.arange(1.0, max_re, find_distance_between_two_points(1, max_re) / frames_number)
    min_im_range = np.arange(-1.2, min_im, find_distance_between_two_points(-1.2, min_im) / frames_number)

    for i in range(frames_number):
        print(min_re_range[i], max_re_range[i], min_im_range[i])
        new_frame_matrix = create_mandelbrot_matrix(height, width, min_re_range[i], max_re_range[i], min_im_range[i],
                                                    500)
        new_frame = create_image_from_matrix(height, width, new_frame_matrix)
        frames.append(new_frame)
        print(f"created frame {i}")
        new_frame.save(f'images/mandelbrot_{i}.png')
    return frames


if __name__ == "__main__":
    # create_mandelbrot_image(500, 500).save('images/mandelbrot.png')
    # frames = create_mandelbrot_gif_frames(60, 500, 500, -1.253667535896, -1.253497120720, -0.384432435761)
    theta = 71
    r = 0.25
    x = r * math.cos(theta) - 1
    y = r * math.sin(theta)
    frames = create_mandelbrot_gif_frames(300, 700, 700, x - 0.000015, x + 0.000015, y - 0.000015)
    frames[0].save('images/mandelbrot.gif', format='GIF', append_images=frames[1:], save_all=True, duration=20, loop=0)
