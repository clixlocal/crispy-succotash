
def is_etree_list(children):
  all_tags = list(map(lambda t: t.tag, children))
  return len(all_tags) == 1 or not len(all_tags) == len(set(all_tags))

def etree_to_dict(t):
  children = t.getchildren()
  if len(children) > 0:
    if is_etree_list(children):
      d = {t.tag : map(etree_to_dict, children)}
    else:
      d = {}
      for child in children:
        if len(child.getchildren()) > 0:
          d[child.tag] = etree_to_dict(child)
        else:
          d[child.tag] = child.text
  else:
    d = {t.tag: t.text}
  return d

