from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    '''
    Custom permission that's allow anyone only read project_db_api. For security reasons.
    '''

    def has_permission(self, request, views):
        if request.method == 'GET' or request.method == 'OPTIONS':
            return True