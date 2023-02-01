# from django.test import TestCase
# from addressee.models import Addressee
#
#
# # models test
# class AddresseeTest(TestCase):
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def create_whatever(self, name, phone_number, tags):
#         return Addressee.objects.create(
#             name=name,
#             phone_number=phone_number,
#             tags=tags
#         )
#
#     def test_addressee_creation(self):
#         name = "Taster"
#         phone_number = 79998887766
#         tags = ('test', 'ok')
#
#         a = self.create_whatever(name=name, phone_number=phone_number, tags=tags)
#         self.assertTrue(isinstance(a, Addressee))
#         self.assertEqual(a.name, name)
#         self.assertEqual(a.phone_number, phone_number)
