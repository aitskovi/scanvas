import argparse
from PIL import Image

# Split into an image into 'n' slices of equal size.
def split(image, num_slices):
  """
    Split an image into 'n' slices of equal size. Does
    not account for rounding so can lose some of the edges
    of the image.
  """
  width, height = image.size
  slice_width = width / num_slices

  slices = []
  for i in range(num_slices):
    box = (i * slice_width, 0, (i + 1) * slice_width, height)
    slices.append(image.crop(box))

  return slices


def extend(image, border):
  """
    Extend the edges of the image a certain number of pixes
    on each side.
  """
  width, height = image.size

  extended_width = width + 2 * border
  extended_height = height + 2 * border
  extended_image = Image.new("RGB", (extended_width, extended_height))
  extended_image.paste(image, (border, border, border + width, border + height))
  
  # Right Edge
  right_edge_box = (width - border, 0, width, height)
  right_edge_image = image.copy().crop(right_edge_box).transpose(Image.FLIP_LEFT_RIGHT)
  extended_image.paste(right_edge_image, (width + border, border, width + 2 * border, height + border))

  # Left Edge
  left_edge_box = (0, 0, border, height)
  left_edge_image = image.copy().crop(left_edge_box).transpose(Image.FLIP_LEFT_RIGHT)
  extended_image.paste(left_edge_image, (0, border, border, border + height))

  # Top Edge
  top_edge_box = (0, border, extended_width, border * 2)
  top_edge_image = extended_image.copy().crop(top_edge_box).transpose(Image.FLIP_TOP_BOTTOM)
  extended_image.paste(top_edge_image, (0, 0, extended_width, border))

  # Bottom Edge
  bottom_edge_box = (0, height, extended_width, border + height)
  bottom_edge_image = extended_image.copy().crop(bottom_edge_box).transpose(Image.FLIP_TOP_BOTTOM)
  extended_image.paste(bottom_edge_image, (0, border + height, extended_width, extended_height))

  return extended_image

if __name__ == '__main__':
  description = "Split an image into panels for canvas printing"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('image')

  args = parser.parse_args()
  image_name = args.image

  image = Image.open(image_name)
  splits = split(image, 3)
  for split in splits:
    extend(split, 300).show()
