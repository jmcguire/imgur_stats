import web
from bokeh.embed import components
from plot_contributions import weekly_plot_of_user

render = web.template.render('templates/', base='_base')

urls = (
  '/', 'index',
)

class index:

  form = web.form.Form(
    web.form.Textbox('username', web.form.notnull, description="Imgur username"),
    web.form.Button('Graph'),
  )

  def GET(self):
    form = self.form()
    if not form.validates():
      return render.index(form)
    else:
      username = form.d.username
      plot = weekly_plot_of_user(username)
      script, div = components(plot)
      return render.userplot(username, script, div)

if __name__ == '__main__':
  app = web.application(urls, globals())
  app.run()

