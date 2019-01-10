"""
Test course_catalog serializers
"""
from django.test import TestCase
from .serializers import OCWCourseSerializer


class OCWSerializerTest(TestCase):
    """
    Tests OCWSerializer
    """
    def test_deserializing_a_valid_ocw_course(self):
        """
        Verify that OCWSerializer successfully de-serialize a JSON object and create Course model instance
        """
        valid_ocw_course_master_obj = {
            'uid': 'e9387c256bae4ca99cce88fd8b7f8272',
            'title': 'Undergraduate Thesis Tutorial',
            'description': '<p>This course is a series of lectures on prospectus and thesis writing</p>',
            'course_level': 'Undergraduate',
            'from_semester': 'Fall',
            'from_year': '2015',
            'language': 'en-US',
            'image_src': 'https://s3.us-east-2.amazonaws.com/alizagarantestbucket/test_folder/'
                         'f49d46243a5c035597e75941ffec830a_22-thtf15.jpg',
            'image_description': 'Photo of hardbound academic theses on library shelves.',
            'platform': 'OCW',
            'creation_date': '2016-01-08 22:35:55.151996+00:00',
            'expiration_date': None,
            'raw_json': {'name': 'ali', 'whatever': 'something', 'llist': [1, 2, 3]},
            'instructors': [
                {
                    'middle_initial': '',
                    'first_name': 'Michael',
                    'last_name': 'Short',
                    'suffix': '',
                    'title': '',
                    'mit_id': '',
                    'department': '',
                    'directory_title': '',
                    'uid': 'd9ca5631c6936252866d63683c0c452e'
                },
                {
                    'middle_initial': '',
                    'first_name': 'Jane',
                    'last_name': 'Kokernak',
                    'suffix': '',
                    'title': '',
                    'mit_id': '',
                    'department': '',
                    'directory_title': '',
                    'uid': 'bb1e26b5f5c9c054ddae8a2988ad7b42'
                },
                {
                    'middle_initial': '',
                    'first_name': 'Christine',
                    'last_name': 'Sherratt',
                    'suffix': '',
                    'title': '',
                    'mit_id': '',
                    'department': '',
                    'directory_title': '',
                    'uid': 'a39f692061a70a105c25b15374c02c92'
                }
            ],
            'course_collections': [
                {
                    'ocw_feature': 'Engineering',
                    'ocw_subfeature': 'Nuclear Engineering',
                    'ocw_feature_url': '',
                    'ocw_speciality': '',
                    'ocw_feature_notes': ''
                },
                {
                    'ocw_feature': 'Humanities',
                    'ocw_subfeature': 'Literature',
                    'ocw_feature_url': '',
                    'ocw_speciality': 'Academic Writing',
                    'ocw_feature_notes': ''
                }
            ],
            'price': {
                'price': 0.0,
                'mode': 'audit',
                'upgrade_deadline': None
            }
        }
        serializer = OCWCourseSerializer(data=valid_ocw_course_master_obj)
        self.assertTrue(
            serializer.is_valid()
        )

    def test_deserialzing_an_invalid_ocw_course(self):
        """
        Verifies that OCWSerializer validation works correctly if the OCW course has invalid values
        """
        invalid_ocw_course_master_obj = {
            'uid': '',
            'title': '',
            'description': '',
            'course_level': '',
            'from_semester': 'Fall',
            'from_year': '2015',
            'language': 'en-US',
            'image_src': '',
            'image_description': 'Photo of hardbound academic theses on library shelves.',
            'platform': 'OCW',
            'creation_date': '2016/01/08 22:35:55.151996+00:00',
            'expiration_date': None,
            'raw_json': {},
            'instructors': [
                {
                    'middle_initial': '',
                    'first_name': 'Michael',
                    'suffix': '',
                    'title': '',
                    'mit_id': '',
                    'department': '',
                    'directory_title': '',
                    'uid': 'd9ca5631c6936252866d63683c0c453e'
                },
                {
                    'middle_initial': '',
                    'first_name': 'Jane',
                    'last_name': 'Kokernak',
                    'suffix': '',
                    'title': '',
                    'mit_id': '',
                    'department': '',
                    'directory_title': '',
                    'uid': 'bb1e26b5f5c9c054ddae8a2988ad7b48'
                },
                {
                    'middle_initial': '',
                    'last_name': 'Sherratt',
                    'suffix': '',
                    'title': '',
                    'mit_id': '',
                    'department': '',
                    'directory_title': '',
                    'uid': 'a39f692061a70a105c25b15374c02c95'
                }
            ],
            'course_collections': [
                {
                    'ocw_feature': 'Engineering',
                    'ocw_subfeature': 'Nuclear Engineering',
                    'ocw_feature_url': '',
                    'ocw_speciality': '',
                    'ocw_feature_notes': ''
                },
                {
                    'ocw_feature': 'Humanities',
                    'ocw_subfeature': 'Literature',
                    'ocw_feature_url': '',
                    'ocw_speciality': 'Academic Writing',
                    'ocw_feature_notes': ''
                }
            ],
            'price': {
                'price': 0.0,
                'upgrade_deadline': None
            }
        }
        serializer = OCWCourseSerializer(data=invalid_ocw_course_master_obj)
        self.assertFalse(
            serializer.is_valid()
        )
