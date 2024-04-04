from src.core.services.base_servises import BaseServices
from src.app.product.models import Admins


class AdminsService(BaseServices):
    model = Admins


admin_service = AdminsService()
