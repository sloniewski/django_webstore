from django.contrib.auth.mixins import UserPassesTestMixin


class StaffOnlyMixin(UserPassesTestMixin):
    login_url = '/dashboard/users_panel/login'

    def test_func(self):
        return self.request.user.is_staff
