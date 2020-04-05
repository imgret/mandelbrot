from PIL import Image
import numpy as np
import math


def create_mandelbrot_image(height, width, min_re=-2.0, max_re=1.0, min_im=-1.2, max_iterations=50):
    image = Image.new("RGB", (width, height), color="white")

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
                    image.putpixel((x, y), (intensity, intensity, intensity))
                    break
                z_im = 2 * z_re * z_im + c_im
                z_re = z_re2 - z_im2 + c_re
            if is_inside:
                image.putpixel((x, y), (0, 0, 0))
    return image


def create_mandelbrot_gif(frames_number, height, width, min_re, max_re, min_im):
    frames = list()
    min_re_range = np.arange(-2.0, min_re, abs(min_re / frames_number))
    max_re_range = np.arange(1.0, max_re, max_re / frames_number)
    min_im_range = np.arange(-1.2, min_im, abs(min_im / frames_number))

    for i in range(frames_number):
        new_frame = create_mandelbrot_image(height, width,
                                            min_re_range[i],
                                            max_re_range[i],
                                            min_im_range[i],
                                            100 + 100 * i)
        frames.append(new_frame)
        print(f"created frame {i}")
        new_frame.save(f'images/mandelbrot_{i}.png')
    return frames


if __name__ == "__main__":
    # create_mandelbrot_image(500, 500).save('images/mandelbrot.png')
    frames = create_mandelbrot_gif(60, 250, 250, -1.253667535896, -1.253497120720, -0.384432435761)
    # for i, frame in enumerate(frames, 1):
    #     frame.save(f'mandelbrot_{i}.png')
    # frames[0].save('images/mandelbrot.gif', format='GIF', append_images=frames[1:], save_all=True, duration=1000, loop=0)
