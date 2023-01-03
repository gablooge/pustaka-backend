from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from library.models import Book
from users.models import User


class CreateBookTestCase(TestCase):
    def setUp(self):
        # librarian
        self.librarian = User.objects.create_superuser(
            username="test_librarian",
            role=User.UserTypes.LIBRARIAN,
            email="test_librarian@test.com",
            password=settings.TEST_PASSWORD,
        )
        self.librarian.save()

        login_response = self.client.post(
            reverse("users_api:token_login"),
            data={"username": self.librarian.email, "password": settings.TEST_PASSWORD},
            content_type="application/json",
        )
        self.librarian_token = login_response.json()

        # student
        self.student = User.objects.create(email="student@gmail.com")
        self.student.username = "student"
        self.student.role = User.UserTypes.STUDENT
        self.student.set_password(settings.TEST_PASSWORD)
        self.student.save()

        login_response = self.client.post(
            reverse("users_api:token_login"),
            data={"username": self.student.email, "password": settings.TEST_PASSWORD},
            content_type="application/json",
        )
        self.student_token = login_response.json()

        self.valid_payload = {
            "title": "Dynamic Programming: A Computational Tool",
            "summary": (
                "Dynamic programming has long been applied to numerous areas in mat- matics"
                ", science, engineering, business, medicine, information systems, b- mathematics"
                ", arti?cial intelligence, among others. Applications of dynamic programming"
                " have increased as recent advances have been made in areas such as neural"
                " networks, data mining, soft computing, and other areas of com- tational"
                " intelligence. The value of dynamic programming formulations and means to"
                " obtain their computational solutions has never been greater. This book"
                " describes the use of dynamic programming as a computational tool to solve"
                " discrete optimization problems. (1) We ?rst formulate large classes of discrete"
                " optimization problems in dynamic programming terms, speci?cally by deriving the"
                " dynamic progr- ming functional equations (DPFEs) that solve these problems."
                " A text-based language, gDPS, for expressing these DPFEs is introduced. gDPS may"
                " be regarded as a high-level speci?cation language, not a conventional procedural"
                " computer programming language, but which can be used to obtain numerical solutions"
                ". (2)Wethende?neandexaminepropertiesofBellmannets,aclassofPetri nets that serves"
                " both as a formal theoretical model of dynamic programming problems, and as an"
                " internal computer data structure representation of the DPFEs that solve these"
                " problems. (3)Wealsodescribethedesign,implementation,anduseofasoftwaretool,"
                " calledDP2PN2Solver, for solving DPFEs. DP2PN2Solver may be regarded as a program"
                " generator, whose input is a DPFE, expressed in the input spec- cation language"
                " gDPS and internally represented as a Bellman net, and whose output is its numerical"
                " solution that is produced indirectly by the generation of “solver” code, which when"
                " executed yields the desired solution."
            ),
            "author": "Art Lew,Holger Mauch",
            "number": 6,
        }

        self.test_create_by_librarian()

    def test_create_by_librarian(self):
        uri = reverse("library_api:Book-list")
        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'
        total = Book.objects.count()
        resp = self.client.post(
            uri,
            data=self.valid_payload,
            content_type="application/json",
        )
        data = resp.json()
        assert data["title"] == "Dynamic Programming: A Computational Tool"
        assert resp.status_code == 201
        assert data["created_by"] == self.librarian.id
        assert Book.objects.count() == total + 1
        assert Book.objects.get(id=data["id"]).created_by == self.librarian

    def test_create_by_student(self):
        uri = reverse("library_api:Book-list")
        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.student_token.get("access")}'
        total = Book.objects.count()
        resp = self.client.post(
            uri,
            data=self.valid_payload,
            content_type="application/json",
        )
        data = resp.json()
        assert resp.status_code == 403
        assert data["detail"] == "You do not have permission to perform this action."
        assert Book.objects.count() == total

    def test_create_wrong_token(self):
        uri = reverse("library_api:Book-list")
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

        resp = self.client.post(
            uri,
            data={},
            content_type="application/json",
        )
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Given token not valid for any token type"

    def test_create_no_token(self):
        uri = reverse("library_api:Book-list")
        self.client.defaults["HTTP_AUTHORIZATION"] = ""
        resp = self.client.post(
            uri,
            data={},
            content_type="application/json",
        )
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Authentication credentials were not provided."

    def test_create_librarian_empty_payload(self):
        uri = reverse("library_api:Book-list")
        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.post(
            uri,
            data={},
            content_type="application/json",
        )
        assert resp.json()["title"][0] == "This field is required."
        assert resp.status_code == 400

    @parameterized.expand(
        [
            # title None
            (None, "test", "test", 9, "title", "This field may not be null."),
            # title blank
            ("", "test", "test", 9, "title", "This field may not be blank."),
        ],
    )
    def test_create_librarian_invalid_payload(
        self, title, summary, author, total, field, error
    ):
        uri = reverse("library_api:Book-list")
        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'
        total = Book.objects.count()
        resp = self.client.post(
            uri,
            data={
                "title": title,
                "summary": summary,
                "author": author,
                "number": total,
            },
            content_type="application/json",
        )

        assert resp.status_code == 400
        assert resp.json()[field][0] == error
        assert Book.objects.count() == total


class GetListBookTestCase(CreateBookTestCase):
    def test_get_list_by_librarian(self):
        uri = reverse("library_api:Book-list")

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert len(data) == Book.objects.count()
        assert "created_by" in data[0]
        assert resp.status_code == 200

    def test_get_list_by_student(self):
        uri = reverse("library_api:Book-list")

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert len(data) == Book.objects.count()
        assert "created_by" in data[0]
        assert resp.status_code == 200

    def test_get_list_wrong_token(self):
        uri = reverse("library_api:Book-list")
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Given token not valid for any token type"
        assert resp.status_code == 401

    def test_get_list_no_token(self):
        uri = reverse("library_api:Book-list")

        self.client.defaults["HTTP_AUTHORIZATION"] = ""

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert len(data) == Book.objects.count()
        assert resp.status_code == 200


class GetDetailBookTestCase(CreateBookTestCase):
    def test_get_detail_by_librarian(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert data["created_by"] == self.librarian.id
        assert resp.status_code == 200

    def test_get_detail_by_student(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.student_token.get("access")}'

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        assert resp.status_code == 200

    def test_get_detail_no_token(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults["HTTP_AUTHORIZATION"] = ""

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        assert resp.status_code == 200

    def test_get_detail_wrong_token(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Given token not valid for any token type"
        assert resp.status_code == 401

    def test_get_detail_invalid_id(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": 1000},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Not found."
        assert resp.status_code == 404


class DeleteBookTestCase(CreateBookTestCase):
    def test_delete_a_book_by_librarian(self):
        total = Book.objects.count()
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.delete(
            uri,
            content_type="application/json",
        )
        assert Book.objects.count() == total - 1
        assert resp.status_code == 204

    def test_delete_a_book_by_student(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.student_token.get("access")}'

        resp = self.client.delete(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "You do not have permission to perform this action."
        assert resp.status_code == 403

    def test_delete_a_book_wrong_token(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

        resp = self.client.delete(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Given token not valid for any token type"
        assert resp.status_code == 401

    def test_delete_a_book_no_token(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults["HTTP_AUTHORIZATION"] = ""

        resp = self.client.delete(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Authentication credentials were not provided."
        assert resp.status_code == 401

    def test_delete_a_book_invalid_id(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": 1000},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.delete(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Not found."
        assert resp.status_code == 404


class UpdateBookTestCase(CreateBookTestCase):
    def test_update_a_book_by_librarian(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.put(
            uri,
            data=self.valid_payload,
            content_type="application/json",
        )
        data = resp.json()
        assert data["created_by"] == self.librarian.id
        assert resp.status_code == 200

    def test_update_a_book_by_student(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.student_token.get("access")}'

        resp = self.client.put(
            uri,
            data=self.valid_payload,
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "You do not have permission to perform this action."
        assert resp.status_code == 403

    def test_update_a_book_wrong_token(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

        resp = self.client.put(
            uri,
            data=self.valid_payload,
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Given token not valid for any token type"
        assert resp.status_code == 401

    def test_update_a_book_no_token(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )

        self.client.defaults["HTTP_AUTHORIZATION"] = ""

        resp = self.client.put(
            uri,
            data=self.valid_payload,
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Authentication credentials were not provided."
        assert resp.status_code == 401

    def test_update_librarian_empty_payload(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )
        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'
        resp = self.client.put(
            uri,
            data={},
            content_type="application/json",
        )
        data = resp.json()
        assert data["title"][0] == "This field is required."
        assert resp.status_code == 400

    @parameterized.expand(
        [
            # title None
            (None, "test", "test", 9, "title", "This field may not be null."),
            # title blank
            ("", "test", "test", 9, "title", "This field may not be blank."),
        ],
    )
    def test_update_librarian_invalid_payload(
        self, title, summary, author, total, field, error
    ):
        total = Book.objects.count()
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": Book.objects.all()[0].id},
        )
        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'
        resp = self.client.put(
            uri,
            data={
                "title": title,
                "summary": summary,
                "author": author,
                "number": total,
            },
            content_type="application/json",
        )
        data = resp.json()

        assert resp.status_code == 400
        assert data[field][0] == error
        assert Book.objects.count() == total

    def test_update_a_book_404(self):
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": 1000},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.put(
            uri,
            data={},
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Not found."
        assert resp.status_code == 404


class BorrowBookTestCase(CreateBookTestCase):
    def test_student_borrow_book_by_librarian(self):
        borrowed_book = Book.objects.all()[0]
        # test check availability stock before book borrowed
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": borrowed_book.id},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        data = resp.json()

        assert data["availability_stock"] == borrowed_book.number
        assert resp.status_code == 200

        # test borrowing a book
        uri = reverse("library_api:Book-borrow", kwargs={"pk": self.student.id})

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.post(
            uri,
            data={"books": [borrowed_book.id]},
            content_type="application/json",
        )
        data = resp.json()
        assert data["books"] == [borrowed_book.id]
        assert resp.status_code == 200

        # test check availability stock
        uri = reverse(
            "library_api:Book-detail",
            kwargs={"pk": borrowed_book.id},
        )

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.get(
            uri,
            content_type="application/json",
        )
        data = resp.json()
        assert data["availability_stock"] == borrowed_book.number - 1
        assert resp.status_code == 200

    def test_student_borrow_book_by_student(self):
        uri = reverse("library_api:Book-borrow", kwargs={"pk": self.student.id})

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.student_token.get("access")}'

        resp = self.client.post(
            uri,
            data={},
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "You do not have permission to perform this action."
        assert resp.status_code == 403

    def test_student_borrow_book_wrong_token(self):
        uri = reverse("library_api:Book-borrow", kwargs={"pk": self.student.id})

        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

        resp = self.client.post(
            uri,
            data={},
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Given token not valid for any token type"
        assert resp.status_code == 401

    def test_student_borrow_book_no_token(self):
        uri = reverse("library_api:Book-borrow", kwargs={"pk": self.student.id})

        self.client.defaults["HTTP_AUTHORIZATION"] = ""

        resp = self.client.post(
            uri,
            data={},
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Authentication credentials were not provided."
        assert resp.status_code == 401

    def test_student_borrow_book_404(self):
        uri = reverse("library_api:Book-borrow", kwargs={"pk": 1000})

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.post(
            uri,
            data={"books": [Book.objects.all()[0].id]},
            content_type="application/json",
        )
        data = resp.json()
        assert data["detail"] == "Not found."
        assert resp.status_code == 404

    def test_student_borrow_book_invalid_payload(self):
        uri = reverse("library_api:Book-borrow", kwargs={"pk": self.student.id})

        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.post(
            uri,
            data={"books": [1000]},
            content_type="application/json",
        )
        data = resp.json()
        assert data["books"][0] == 'Invalid pk "1000" - object does not exist.'
        assert resp.status_code == 400
