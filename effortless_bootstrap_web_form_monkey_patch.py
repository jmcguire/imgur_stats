"""
These are the rendering parts of the web/form.py. These are what need to get overwritten in order to make this thing extendable, bootstappable, yuiable, whatever.
"""

import copy
import web.form
import web.utils as utils, web.net as net

def patch():
  web.form.Form.render = Form_render
  web.form.Form.rendernote = Form_rendernote
  web.form.Input.render = Input_render
  web.form.File.render = File_render
  web.form.Textarea.render = Textarea_render
  web.form.Dropdown.render = Dropdown_render
  web.form.GroupedDropdown.render = GroupedDropdown_render
  web.form.Radio.render = Radio_render
  web.form.Checkbox.render = Checkbox_render
  web.form.Button.render = Button_render

  web.form.Input.group_start = div_form_group
  web.form.Input.group_end = end_div
  web.form.Input.group_title = label
  web.form.Checkbox.group_start = div_form_check
  web.form.Checkbox.group_end = end_label_div
  web.form.Checkbox.group_title = label_checkbox
  web.form.Radio.group_start = fieldset_form_group
  web.form.Radio.group_end = end_fieldset
  web.form.Radio.group_title = legend


# bootstrap specific components for containing inputs

def div_form_group(self):
  return '<div class="form-group">'
def fieldset_form_group(self):
  return '<fieldset class="form-group">'
def div_form_check(self):
  return '<div class="form-check">'

def label(self):
  return '<label id="%s">%s</label>' % (self.id, net.websafe(self.description))
def label_checkbox(self):
  return '<label class="form-check-label">'
def legend(self):
  return '<legend>%s</legend>' % (net.websafe(self.description))

def end_div(self):
  return '</div>'
def end_fieldset(self):
  return '</fieldset>'
def end_label_div(Self):
  return '</label></div>'


def Form_render(self):
  out = ''
  out += self.rendernote(self.note)

  for i in self.inputs:
    if i.is_hidden():
      out += '%s\n' % i.render()
    else:
      out += i.group_start() + "\n"
      out += i.group_title() + "\n"
      out += i.render() + "\n"
      out += i.group_end() + "\n"
      # show utils.safeunicode(i.pre) 
      # show utils.safeunicode(i.post) 
      # show self.rendernote(i.note)
  return out

def Form_rendernote(self, note):
  if note:
    return '<strong class="wrong">%s</strong>' % net.websafe(note)
  else:
    return ""


def Input_render(self):
  attrs = self.attrs.copy()
  attrs['type'] = self.get_type()
  attrs['id'] = self.name
  attrs['name'] = self.name
  attrs['class'] = 'form-control'
  if self.value is not None:
    attrs['value'] = self.value
  return '<input %s>' % attrs


def File_render(self):
  attrs = self.attrs.copy()
  attrs['type'] = self.get_type()
  attrs['id'] = self.name
  attrs['name'] = self.name
  attrs['class'] = 'form-control-file'
  if self.value is not None:
    attrs['value'] = self.value
  return '<input %s>' % attrs


def Textarea_render(self):
  attrs = self.attrs.copy()
  attrs['id'] = self.name
  attrs['name'] = self.name
  attrs['class'] = 'form-control'
  value = net.websafe(self.value or '')
  return '<textarea %s>%s</textarea>' % (attrs, value)


def Dropdown_render(self):
  attrs = self.attrs.copy()
  attrs['id'] = self.name
  attrs['name'] = self.name
  attrs['class'] = 'form-control'

  out = '<select %s>\n' % attrs
  for arg in self.args:
    out += self._render_option(arg)
  out += '</select>\n'

  return out


def GroupedDropdown_render(self):
  attrs = self.attrs.copy()
  attrs['id'] = self.name
  attrs['name'] = self.name
  attrs['class'] = 'form-control'

  out = '<select %s>\n' % attrs

  for label, options in self.args:
    out += '  <optgroup label="%s">\n' % net.websafe(label)
    for arg in options:
      out += self._render_option(arg, indent = '    ')
    out +=  '  </optgroup>\n'

  out += '</select>\n'
  return out


def Radio_render(self):
  out = ''

  for arg in self.args:
    out += '<div class="form-check">'
    out += '<label class="form-check-label">'

    if isinstance(arg, (tuple, list)):
      value, desc= arg
    else:
      value, desc = arg, arg 
    attrs = self.attrs.copy()
    attrs['name'] = self.name
    attrs['id'] = self.name
    attrs['name'] = self.name
    attrs['type'] = 'radio'
    attrs['value'] = value
    attrs['class'] = 'form-check-input'
    if self.value == value:
      attrs['checked'] = 'checked'
    out += '<input %s/> %s' % (attrs, net.websafe(desc))

    out += '</label></div>'

  return out

def Checkbox_render(self):
  attrs = self.attrs.copy()
  attrs['type'] = 'checkbox'
  attrs['id'] = self.name
  attrs['name'] = self.name
  attrs['value'] = self.value

  if self.checked:
    attrs['checked'] = 'checked'
  return '<input %s> %s' % (attrs, net.websafe(desc))


def Button_render(self):
  attrs = self.attrs.copy()
  attrs['id'] = self.name
  attrs['name'] = self.name
  attrs['class'] = 'btn btn-primary'
  attrs['type'] = 'submit'
  if self.value is not None:
    attrs['value'] = self.value
  html = attrs.pop('html', None) or net.websafe(self.name)
  return '<button %s>%s</button>' % (attrs, html)


