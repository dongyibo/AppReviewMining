# -- coding: utf-8 --
import web

from controller.controller import Controller
from util import db_const as const, pagination

urls = (
    '/', 'Index',
    '/showSuggestion', 'Suggestion',
    '/abortAjax', 'AbortAjax',
    '/recoverAjax', 'RecoverAjax',
    '/abortBug', 'AbortBug',
    '/abortSuggestion', 'AbortSuggestion'
)
app = web.application(urls, globals())

render = web.template.render('templates')

p = pagination.Pagination()


class AbortAjax:
    def GET(self):
        category = web.input()['category']
        id = web.input()['id']
        appId = web.input()['appId']
        # print id, category
        Controller.abort(id, int(category), int(appId))
        return id


class RecoverAjax:
    def GET(self):
        category = web.input()['category']
        id = web.input()['id']
        appId = web.input()['appId']
        # print id, category
        Controller.recover(id, int(category), int(appId))
        return id


class Index:
    def GET(self):
        storage = web.input()
        if not storage:
            page = 1
            appId = 482
        else:
            page = int(storage['page'])
            appId = int(storage['appId'])

        bugs = Controller.prioritize_data(const.BUG, appId)
        p.set_property(bugs, page)
        data = p.get_page_of_data()
        maxPage = p.get_total_pages()
        return render.index(data, const.BUG, page, maxPage, appId)


class Suggestion:
    def GET(self):
        storage = web.input()
        if not storage:
            page = 1
            appId = 482
        else:
            page = int(storage['page'])
            appId = int(storage['appId'])
        # print page,appId
        suggestions = Controller.prioritize_data(const.FEATURE, appId)
        p.set_property(suggestions, page)
        data = p.get_page_of_data()
        maxPage = p.get_total_pages()
        return render.index(data, const.FEATURE, page, maxPage, appId)


class AbortBug:
    def GET(self):
        storage = web.input()
        if not storage:
            page = 1
            appId = 482
        else:
            page = int(storage['page'])
            appId = int(storage['appId'])

        bugs = Controller.prioritize_data_aborted(const.BUG, appId)
        p.set_property(bugs, page)
        data = p.get_page_of_data()
        maxPage = p.get_total_pages()
        return render.index(data, const.BUG_ABORTED, page, maxPage, appId)


class AbortSuggestion:
    def GET(self):
        storage = web.input()
        if not storage:
            page = 1
            appId = 482
        else:
            page = int(storage['page'])
            appId = int(storage['appId'])

        suggestions = Controller.prioritize_data_aborted(const.FEATURE, appId)
        p.set_property(suggestions, page)
        data = p.get_page_of_data()
        maxPage = p.get_total_pages()
        return render.index(data, const.FEATURE_ABORTED, page, maxPage, appId)


if __name__ == "__main__":
    app.run()
