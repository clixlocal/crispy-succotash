import datetime, pdb
from collections import defaultdict

def is_etree_list(children):
  all_tags = list(map(lambda t: t.tag, children))
  return len(all_tags) == 1 or len(set(all_tags)) == 1

def etree_child(child):
  if len(child.getchildren()) > 0:
    return etree_to_dict(child)
  else:
    return child.text

def etree_to_dict(t):
  children = t.getchildren()
  if len(children) > 0:
    if is_etree_list(children):
      d = {t.tag : map(etree_to_dict, children)}
    else:
      sub = {}
      d = {t.tag: sub}
      tag_counts = defaultdict(int)
      for child in children:
        tag_counts[child.tag] = tag_counts[child.tag] + 1
      for child in children:
        if tag_counts[child.tag] > 1:
          if not sub.get(child.tag):
            sub[child.tag] = []
          sub[child.tag].append(etree_child(child))
        else:
          sub[child.tag] = etree_child(child)
  else:
    d = {t.tag: t.text}
  return d

def unix_time(dt):
  epoch = datetime.datetime.utcfromtimestamp(0)
  delta = dt - epoch
  return delta.total_seconds()

def unix_time_millis(dt):
  return unix_time(dt) * 1000.0
