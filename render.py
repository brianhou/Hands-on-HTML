from yattag import Doc

def render_json(data):
  """Returns the contents of the page."""
  doc, tag, text = Doc().tagtext()
  def create_div(photo_id, top, left, width, aspect_ratio, path):
    width = '{}%'.format(100 * width)
    with tag('div', klass="magic"):
      doc.stag('img', width=width, src=path, id=photo_id)
    num_files = data['num_images']
  for image_id, datum in data['images'].items():
    top, left = datum['top'], datum['left']
    width, aspect = datum['width'], datum['aspect-ratio']
    path = datum['path']
    create_div(str(image_id), top, left, width, aspect, path)
  return doc.getvalue()
