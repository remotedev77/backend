from rest_framework import permissions
from users.models import  User


class CheckFinalTestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if User.PlanChoices.basic == request.user.plan:
            if request.user.statistics.count() >= 150:
                request.user.final_test = True
                request.user.save()
                return request.user.final_test
            else:
                request.user.final_test = False
                request.user.save()
                return request.user.final_test
            

        elif User.PlanChoices.pro == request.user.plan:
            if request.user.final_test == True:
                return request.user.final_test
            
            if request.user.statistics.count() >= 150:
                request.user.final_test = True
                request.user.save()
                return request.user.final_test
            return False

