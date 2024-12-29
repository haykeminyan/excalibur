from apps.deduction.mixins import BaseDeductionExportDocx
from apps.deduction.views import DeductionListView, DeductionDetailView, AddDeduction, UpdateDeduction, DeleteDeduction
from apps.facture.mixins import BaseFactureLocalExportDocx, BaseFactureWorldExportDocx
from apps.facture.views import LocalFactureListView, WorldFactureListView, UpdateLocalFacture, UpdateWorldFacture, \
	AddWorldFacture, AddLocalFacture, LocalFactureDetailView, WorldFactureDetailView, DeleteLocalFacture, \
	DeleteWorldFacture
from apps.main.views import MainMenuListView
from apps.users.views import LogoutUser, LoginUser

url_names_from_deduction = [
    'apps.deduction:list',
    'apps.deduction:detail',
    'apps.deduction:create',
    'apps.deduction:edit',
    'apps.deduction:delete',
    'apps.deduction:generate-deduction-docx',
]

url_names_from_facture = [
	 'apps.facture:local_create',
	 'apps.facture:world_create',
	 'apps.facture:local_update',
	 'apps.facture:world_update',
	 'apps.facture:local_delete',
	 'apps.facture:world_delete',
	 'apps.facture:local_list',
	 'apps.facture:world_list',
	 'apps.facture:local_detail',
	 'apps.facture:world_detail',
	 'apps.facture:generate-local-docx',
	 'apps.facture:generate-world-docx'
]

url_names_from_users = [
	'apps.users:login',
	'apps.users:logout'
]

url_names_from_main = [
	'apps.main:main_menu'
]

url_names_from_fail = [
	'apps.main:fail'
]

url_to_view_mapping = {
	'apps.facture:local_list': LocalFactureListView,
	'apps.facture:world_list': WorldFactureListView,
	'apps.facture:local_create': AddLocalFacture,
	'apps.facture:world_create': AddWorldFacture,
	'apps.facture:local_update': UpdateLocalFacture,
	'apps.facture:world_update': UpdateWorldFacture,
	'apps.facture:local_detail': LocalFactureDetailView,
	'apps.facture:world_detail': WorldFactureDetailView,
	'apps.facture:local_delete': DeleteLocalFacture,
	'apps.facture:world_delete': DeleteWorldFacture,
	'apps.deduction:list': DeductionListView,
	'apps.deduction:detail': DeductionDetailView,
	'apps.deduction:create': AddDeduction,
	'apps.deduction:edit': UpdateDeduction,
	'apps.deduction:delete': DeleteDeduction,
	'apps.facture:generate-local-docx': BaseFactureLocalExportDocx,
	'apps.facture:generate-world-docx': BaseFactureWorldExportDocx,
	'apps.deduction:generate-deduction-docx': BaseDeductionExportDocx,
	'apps.users:login': LoginUser,
	'apps.users:logout': LogoutUser,
	'apps.main:main_menu': MainMenuListView,
}