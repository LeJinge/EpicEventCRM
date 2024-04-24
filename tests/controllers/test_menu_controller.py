import pytest
from unittest.mock import patch
from typer.testing import CliRunner

from controllers.logout_controller import logout
from models.models import User, UserRole
from controllers.menu_controller import navigate_main_menus, navigate_user_menu


class TestNavigateMainMenuAsSuperuser:
    @pytest.fixture
    def superuser(self):
        return User(email='superuser@example.com', role=UserRole.SUPERUSER)

    @pytest.fixture(autouse=True)
    def setup_method(self, tmpdir):
        self.runner = CliRunner()
        # self.superuser = User(email='superuser@example.com', password='password', role='SUPERUSER')
        self.mock_prompt_patcher = patch('typer.prompt')
        self.mock_prompt = self.mock_prompt_patcher.start()
        self.cwd = tmpdir.mkdir("testdir")
        self.cwd.chdir()

    def teardown_method(self):
        self.mock_prompt_patcher.stop()

    def test_navigate_main_menus_quit(self, superuser):
        self.mock_prompt.return_value = '0'
        with patch('controllers.menu_controller.logout') as mock_logout:
            navigate_main_menus(superuser)
            mock_logout.assert_called_once()

    def test_navigate_main_menus_search(self, superuser):
        self.mock_prompt.side_effect = ['1', '0']
        with patch('controllers.menu_controller.navigate_search_menu') as mock_navigate_search:
            navigate_main_menus(superuser)
            mock_navigate_search.assert_called_once()

    def test_navigate_main_menus_user_menu(self, superuser):
        self.mock_prompt.side_effect = ['2', '0']  # Assurez-vous de toujours permettre la sortie de la boucle while.
        with patch('controllers.menu_controller.navigate_user_menu') as mock_navigate_user:
            navigate_main_menus(superuser)
            mock_navigate_user.assert_called_once()

    def test_navigate_main_menus_client_menu(self, superuser):
        self.mock_prompt.side_effect = ['3', '0']
        with patch('controllers.menu_controller.navigate_client_menu') as mock_navigate_client:
            navigate_main_menus(superuser)
            mock_navigate_client.assert_called_once()

    def test_navigate_main_menus_contract_menu(self, superuser):
        self.mock_prompt.side_effect = ['4', '0']
        with patch('controllers.menu_controller.navigate_contract_menu') as mock_navigate_contract:
            navigate_main_menus(superuser)
            mock_navigate_contract.assert_called_once()

    def test_navigate_main_menus_event_menu(self, superuser):
        self.mock_prompt.side_effect = ['5', '0']
        with patch('controllers.menu_controller.navigate_event_menu') as mock_navigate_event:
            navigate_main_menus(superuser)
            mock_navigate_event.assert_called_once()


class TestNavigateMainMenuAsGestionUser:
    @pytest.fixture
    def gestion(self):
        return User(email='gestion@example.com', role=UserRole.GESTION)

    @pytest.fixture(autouse=True)
    def setup_method(self, tmpdir):
        self.runner = CliRunner()
        self.mock_prompt_patcher = patch('typer.prompt')
        self.mock_prompt = self.mock_prompt_patcher.start()
        self.cwd = tmpdir.mkdir("testdir")
        self.cwd.chdir()

    def teardown_method(self):
        self.mock_prompt_patcher.stop()

    def test_navigate_main_menus_quit(self, gestion):
        self.mock_prompt.return_value = '0'
        with patch('controllers.menu_controller.logout') as mock_logout:
            navigate_main_menus(gestion)
            mock_logout.assert_called_once()

    def test_navigate_main_menus_search(self, gestion):
        self.mock_prompt.side_effect = ['1', '0']
        with patch('controllers.menu_controller.navigate_search_menu') as mock_navigate_search:
            navigate_main_menus(gestion)
            mock_navigate_search.assert_called_once()

    def test_navigate_main_menus_user_menu(self, gestion):
        self.mock_prompt.side_effect = ['2', '0']  # Assurez-vous de toujours permettre la sortie de la boucle while.
        with patch('controllers.menu_controller.navigate_user_menu') as mock_navigate_user:
            navigate_main_menus(gestion)
            mock_navigate_user.assert_called_once()

    def test_navigate_main_menus_contract_menu(self, gestion):
        self.mock_prompt.side_effect = ['3', '0']
        with patch('controllers.menu_controller.navigate_contract_menu') as mock_navigate_contract:
            navigate_main_menus(gestion)
            mock_navigate_contract.assert_called_once()

    def test_navigate_main_menus_event_menu(self, gestion):
        self.mock_prompt.side_effect = ['4', '0']
        with patch('controllers.menu_controller.navigate_event_menu') as mock_navigate_event:
            navigate_main_menus(gestion)
            mock_navigate_event.assert_called_once()


class TestNavigateMainMenuAsCommercialeUser:
    @pytest.fixture
    def commercial(self):
        return User(email='commercial@example.com', role=UserRole.COMMERCIALE)

    @pytest.fixture(autouse=True)
    def setup_method(self, tmpdir):
        self.runner = CliRunner()
        # self.superuser = User(email='superuser@example.com', password='password', role='SUPERUSER')
        self.mock_prompt_patcher = patch('typer.prompt')
        self.mock_prompt = self.mock_prompt_patcher.start()
        self.cwd = tmpdir.mkdir("testdir")
        self.cwd.chdir()

    def teardown_method(self):
        self.mock_prompt_patcher.stop()

    def test_navigate_main_menus_quit(self, commercial):
        self.mock_prompt.return_value = '0'
        with patch('controllers.menu_controller.logout') as mock_logout:
            navigate_main_menus(commercial)
            mock_logout.assert_called_once()

    def test_navigate_main_menus_search(self, commercial):
        self.mock_prompt.side_effect = ['1', '0']
        with patch('controllers.menu_controller.navigate_search_menu') as mock_navigate_search:
            navigate_main_menus(commercial)
            mock_navigate_search.assert_called_once()

    def test_navigate_main_menus_client_menu(self, commercial):
        self.mock_prompt.side_effect = ['2', '0']
        with patch('controllers.menu_controller.navigate_client_menu') as mock_navigate_client:
            navigate_main_menus(commercial)
            mock_navigate_client.assert_called_once()

    def test_navigate_main_menus_contract_menu(self, commercial):
        self.mock_prompt.side_effect = ['3', '0']
        with patch('controllers.menu_controller.navigate_contract_menu') as mock_navigate_contract:
            navigate_main_menus(commercial)
            mock_navigate_contract.assert_called_once()

    def test_navigate_main_menus_event_menu(self, commercial):
        self.mock_prompt.side_effect = ['4', '0']
        with patch('controllers.menu_controller.navigate_event_menu') as mock_navigate_event:
            navigate_main_menus(commercial)
            mock_navigate_event.assert_called_once()


class TestNavigateMainMenuAsSupportUser:
    @pytest.fixture
    def support(self):
        return User(email='support@example.com', role=UserRole.SUPPORT)

    @pytest.fixture(autouse=True)
    def setup_method(self, tmpdir):
        self.runner = CliRunner()
        # self.superuser = User(email='superuser@example.com', password='password', role='SUPERUSER')
        self.mock_prompt_patcher = patch('typer.prompt')
        self.mock_prompt = self.mock_prompt_patcher.start()
        self.cwd = tmpdir.mkdir("testdir")
        self.cwd.chdir()

    def teardown_method(self):
        self.mock_prompt_patcher.stop()

    def test_navigate_main_menus_quit(self, support):
        self.mock_prompt.return_value = '0'
        with patch('controllers.menu_controller.logout') as mock_logout:
            navigate_main_menus(support)
            mock_logout.assert_called_once()

    def test_navigate_main_menus_search(self, support):
        self.mock_prompt.side_effect = ['1', '0']
        with patch('controllers.menu_controller.navigate_search_menu') as mock_navigate_search:
            navigate_main_menus(support)
            mock_navigate_search.assert_called_once()

    def test_navigate_main_menus_event_menu(self, support):
        self.mock_prompt.side_effect = ['2', '0']
        with patch('controllers.menu_controller.navigate_event_menu') as mock_navigate_event:
            navigate_main_menus(support)
            mock_navigate_event.assert_called_once()


class TestNavigateUserMenuAsSuperuser:
    @pytest.fixture
    def superuser(self):
        return User(email='superuser@example.com', role=UserRole.SUPERUSER)

    @pytest.fixture(autouse=True)
    def setup_method(self, tmpdir):
        self.runner = CliRunner()
        self.mock_prompt_patcher = patch('typer.prompt')
        self.mock_prompt = self.mock_prompt_patcher.start()
        self.cwd = tmpdir.mkdir("testdir")
        self.cwd.chdir()

    def teardown_method(self):
        self.mock_prompt_patcher.stop()

    def test_navigate_user_menu_add_user(self, superuser):
        self.mock_prompt.side_effect = ['1', '0']
        with patch('controllers.menu_controller.add_user') as mock_add_user:
            navigate_user_menu(superuser)
            mock_add_user.assert_called_once()

    def test_navigate_user_menu_to_search_menu(self, superuser):
        self.mock_prompt.side_effect = ['2', '0']
        with patch('controllers.menu_controller.navigate_user_search_menu') as mock_search_user:
            navigate_user_menu(superuser)
            mock_search_user.assert_called_once()

