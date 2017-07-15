from django.test import TestCase
from lists.views import home_page
from django.urls.base import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


# from django.core.urlresolvers import resolve

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    #         self.assertTrue(response.content.startswith(b'<html>'))
    # startswith是内建函数str的方法
    #         self.assertIn(b'<title>To-Do lists</title>', response.content)
    #         self.assertTrue(response.content.endswith(b'</html>'))


    #此代码可删除 --2017/04/04
    # def test_home_page_only_saves_items_when_necessary(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(),0)

    #此测试代码已无效  --2017/4/3
    # def test_home_page_display_all_list_items(self):
    #     Item.objects.create(text='itemey1')
    #     Item.objects.create(text='itemey2')
    #
    #     request = HttpRequest()
    #     response = home_page(request)
    #
    #     self.assertIn('itemey1',response.content.decode())
    #     self.assertIn('itemey2',response.content.decode())


#class ItemModelTest(TestCase):
class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(first_saved_item.list,list_)
        self.assertEqual(second_saved_item.text,'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):
    # 提示ValueError: invalid literal for int() with base 10: 'the-only-list-in-the-world'  书上没有说明如何解决，容后研究
    # --2017/04/04
    # def test_uses_list_template(self):
    #     view_list = List.objects.first()
    #     response = self.client.get('/lists/the-only-list-in-the-world/')
    #     print('response',response)
    #     self.assertTemplateUsed(response, 'list.html')

    def test_display_all_list_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey1', list=correct_list)
        Item.objects.create(text='itemey2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item1', list=other_list)
        Item.objects.create(text='other list item2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id))

        self.assertContains(response, 'itemey1')
        self.assertContains(response, 'itemey2')
        self.assertNotContains(response, 'other list item1')
        self.assertNotContains(response, 'other list item2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'],correct_list)

class NewListTest(TestCase):
    #2017/4/3添加该类，此类中的test_save_a_POST_request和test_redirects_after_POST两个方法是从HomePageTest类中拷贝来并修改的
    def test_save_a_POST_request(self):
        # 由于加入了csrf的令牌，会导致测试失败，需要处理，将令牌删除后，则测试通过，必须要删除，注释的话依然会失败
        # 单元测试中，可以不需要令牌，在进行功能测试时，需要将令牌加入
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST['item_text'] = 'A new list item'

        # response = home_page(request)
        #以上四行代码，以下一行可以替代
        self.client.post('/lists/new',data={'item_text':'A new list item'})

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')


        # self.assertIn('A new list item', response.content.decode())
        # expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
        # self.assertEqual(response.content.decode(), expected_html)

    def test_redirects_after_POST(self):
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST['item_text'] = 'A new list item'
        #
        # response = home_page(request)
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post('/lists/%d/add_item' % (correct_list.id), data={'item_text':'A new item for an existing list'})

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post('/lists/%d/add_item' % (correct_list.id),
                         data={'item_text': 'A new item for an existing list'})
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

