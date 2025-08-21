from django.contrib.admin import AdminSite

class AdminSite(AdminSite):
    site_header = "Skillabyte Admin"
    site_title = "Skillabyte Admin Portal"
    index_title = "Welcome to the Skillabyte Admin Portal"

class SuperAdminSite(AdminSite):
    site_header = "Skillabyte Super Admin"
    site_title = "Skillabyte Super Admin Portal"
    index_title = "Welcome to the Skillabyte Super Admin Portal"

admin_site = AdminSite(name='admin')
super_admin_site = SuperAdminSite(name='super_admin')
