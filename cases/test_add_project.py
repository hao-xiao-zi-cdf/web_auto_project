class TestAddaProject:
    """新增项目页面"""

    def test_01_add_project_success_normal(self):
        """新增项目成功-项目名称[1-30位非特殊字符] + 所属应用[0-30位非特殊字符] + 项目描述[0-200位字符]"""

    def test_02_add_add_project_fail_name_exist(self):
        """新增项目失败-项目名称已存在"""

    def test_03_add_project_fail_name_empty(self):
        """新增项目失败-项目名称为空"""

    def test_04_add_project_fail_name_len_31(self):
        """新增项目失败-项目名称31位字符"""

    def test_05_add_project_fail_name_spe_char(self):
        """新增项目失败-项目名称包含10位特殊字符"""

    def test_06_add_project_fail_app_len_31(self):
        """新增项目失败-所属应用31位字符"""

    def test_07_add_project_fail_app_spe_char(self):
        """新增项目失败-所属应用包含10位特殊字符"""

    def test_08_add_project_fail_desc_len_201(self):
        """新增项目失败-项目描述201位字符"""