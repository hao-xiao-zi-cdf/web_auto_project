# web_auto_project —— Web UI 自动化测试框架

基于 **pytest + Playwright + Allure** 的 Web UI 自动化测试框架，采用 POM（Page Object Model）页面对象模式设计。
支持全局预登录、多账号上下文隔离、接口 Mock、用例失败现场保留（截图/视频/trace）、Allure 测试报告生成等能力。

## 一、技术栈

| 技术 | 说明 |
| --- | --- |
| Python 3.11 | 开发语言 |
| pytest | 测试框架 |
| Playwright (sync_api) | 浏览器自动化驱动 |
| allure-pytest | 测试报告集成 |
| requests / urllib3 | base_url 连通性校验 |
| python-slugify | 用例ID转文件安全路径 |

## 二、框架结构

```
web_auto_project
├── cases/                  存放测试用例文件目录（相当于testcase）
│   ├── more_accounts/      多账号切换场景用例（独立conftest创建admin上下文）
│   ├── conftest.py         cases目录级fixture（全局预登录、独立上下文、失败截图/视频）
│   ├── test_login.py       登录用例
│   ├── test_register.py    注册用例
│   ├── test_add_project.py 新增项目用例
│   ├── test_project_list.py项目列表用例
│   ├── test_add_module.py  新增模块用例
│   └── test_lenv_list.py   环境列表用例
├── pages/                  页面对象（POM）封装目录（相当于base基础类封装），每个页面一个类
├── data/                   存放测试数据目录（如 login_data.json，可自由增删）
├── mocks/                  接口Mock数据目录（route.fulfill 模拟服务端响应）
├── plugins/                本地插件目录（相当于common公共方法封装）
│   ├── pytest_playwright.py        定制版Playwright插件（截图/视频/trace接入Allure）
│   └── pytest_base_url_plugin.py   base_url插件（提供base_url fixture）
├── utils/                  公共工具方法封装（如读取JSON测试数据）
├── reports/                allure测试报告原始数据目录（--alluredir输出位置）
├── allure_report/          allure测试报告生成目录，HTML可视化报告
├── test-results/           测试产物目录（失败截图、视频、trace.zip）
├── conftest.py             全局操作，名称是固定写法不可更改
├── pytest.ini              pytest框架规范约束，名称是固定写法不可更改
├── requirements.txt        本框架所使用到的第三方库
└── run.py                  主程序入口
```

## 三、运行机制说明

### 1、本地插件覆盖官方插件
`pytest.ini` 中通过 `-p no:playwright` 和 `-p no:base_url` 禁用了官方插件，
再由根目录 `conftest.py` 中的 `pytest_plugins` 注册本地 `plugins` 目录下的同名插件，
目的是在官方插件基础上定制：把失败截图、视频直接附加到 Allure 报告中。
**注意：`pytest.ini` 中的 `-p no:playwright`、`-p no:base_url` 两行不可删除，否则插件冲突报错。**

### 2、全局配置（根目录 conftest.py）
- `pytest_runtest_call` 钩子：自动把**测试类的文档字符串**映射为 `allure.feature`，把**测试方法的文档字符串**映射为 `allure.title`，无需在用例里手写标签。
- `browser_type_launch_args` fixture：覆盖官方插件配置，支持 `--headed` 有头模式，并添加 `--start-maximized` 窗口最大化参数。

### 3、用例级配置（cases/conftest.py）
- `pre_login`（session级）：全局只登录一次（默认账号 p/123456），后续用例复用 cookie，避免每个用例重复登录。
- `fresh_context` / `unlogin_page`：登录、注册类用例使用**独立的干净上下文**，不加载已登录 cookie，避免打开登录页被直接跳转首页。
- `unlogin_page` 同样带上了用例失败截图与视频保留能力，并附加到 Allure 报告。

### 4、多账号场景（cases/more_accounts/conftest.py）
- `admin_context`（module级）：为 admin 账号（admin/123456）单独创建上下文，实现多账号并行操作（如 A 账号建项目、B 账号删项目）。

## 四、用例模板（baseInfo、testCase的关键字——文档字符串不能缺少）

测试类的文档字符串 => Allure 的 feature；测试方法的文档字符串 => Allure 的用例标题，**两者不能缺少**，否则报告中无标题显示。

```python
from pages.login_page import LoginPage
from playwright.sync_api import expect, Page
import pytest


class TestLogin:
    """登录页面"""                      # 类文档字符串 -> allure.feature，不能缺少

    @pytest.fixture(autouse=True)
    def start_for_each(self, unlogin_page: Page):
        """前置：打开登录页；登录/注册类用例使用 unlogin_page 独立上下文"""
        self.login = LoginPage(unlogin_page)
        self.login.navigate()
        yield
        # 后置操作

    def test_01_login_success(self):
        """登录成功-已注册的1位非特殊字符账号 + 6位正确密码"""   # 方法文档字符串 -> allure.title，不能缺少
        # 操作步骤
        self.login.login("p", "123456")
        # 断言验证，根据实际需求选择使用以下哪种断言方式
        expect(self.login.page).to_have_title("首页")           # 页面标题断言
        expect(self.login.page).to_have_url("index.html")       # 页面URL断言
        expect(self.login.locator_username_tip1).to_be_visible()        # 元素可见断言
        expect(self.login.locator_username_tip1).to_contain_text("不能为空")  # 文本包含断言
        expect(self.login.locator_login_btn).not_to_be_enabled()        # 元素不可点击断言
```

### page 对象（上下文）选择说明
| fixture | 适用场景 |
| --- | --- |
| `page` | 常规用例，依赖全局 `pre_login` 登录后的上下文（需在fixture参数中显式声明依赖 `pre_login`） |
| `unlogin_page` | 登录/注册等不需要登录态的用例，独立干净上下文 |
| `admin_context` | 多账号场景，管理员账号上下文（cases/more_accounts/conftest.py） |

## 五、页面对象（POM）模板

每个页面一个类，`__init__` 中定义元素定位器，方法封装页面操作：

```python
from playwright.sync_api import Page


class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.locator_username = page.get_by_label("用 户 名:")
        self.locator_password = page.get_by_label("密     码:")
        self.locator_login_btn = page.locator('text=立即登录')

    def navigate(self):
        self.page.goto("/login.html")   # 只写相对路径，域名由 --base-url 提供

    def login(self, username, password) -> None:
        """完整登录操作"""
        self.locator_username.fill(username)
        self.locator_password.fill(password)
        self.locator_login_btn.click()
```

## 六、参数说明

1）`--base-url`：被测系统地址，在 `pytest.ini` 的 `addopts` 中配置（当前为 http://47.116.12.183），
页面对象中 `goto()` 只写相对路径，切换环境修改该参数即可，也可命令行传参覆盖：

```bash
pytest --base-url=http://你的环境地址
```

2）浏览器与失败现场参数（均在 `pytest.ini` 的 `addopts` 中）：

| 参数 | 说明 |
| --- | --- |
| `--headed` | 有头模式运行（显示浏览器窗口） |
| `--tracing=retain-on-failure` | 用例失败时保留 trace.zip |
| `--screenshot=only-on-failure` | 用例失败时自动截图 |
| `--video=retain-on-failure` | 用例失败时保留录屏视频 |
| `--browser chromium` | 可追加，指定浏览器内核（chromium/firefox/webkit，默认chromium） |
| `--slowmo 1000` | 可追加，放慢操作速度（毫秒），便于观察 |

3）日志：`pytest.ini` 中 `log_cli = true`、`log_cli_level = info` 开启控制台实时日志。

## 七、接口 Mock 说明

`data/mock_api.py` 中以字典形式定义 Mock（url + handler），用例中通过 `page.route()` 拦截请求：

```python
from data.mock_api import mock_project_400

page.route(mock_project_400["url"], mock_project_400["handler"])
# ... 执行页面操作，接口将返回模拟的400响应 ...
page.unroute(mock_project_400["url"])  # 用例结束解除mock
```

新增 Mock 时参照现有格式：`url` 为 glob 匹配模式（如 `**/api/project`），
`handler` 使用 `route.fulfill(status=..., body=...)` 返回，可模拟 200/400/403/500 等各种响应。

## 八、测试数据说明

`data/` 目录存放测试数据（如 `login_data.json`），可用 `utils/tools.py` 中的 `read_json()` 读取，
返回 `[(), (), ...]` 元组列表，直接配合 `@pytest.mark.parametrize` 做数据驱动：

```python
import pytest
from utils.tools import read_json


@pytest.mark.parametrize("username,password,check_message", read_json("login_data.json"))
def test_login(self, username, password, check_message):
    ...
```

**`data` 目录下的文件可自由增删，其他目录文件均不可删除。**

## 九、运行与报告

### 1、主程序入口（run.py）
执行流程：
1. `pytest.main(['--alluredir', './reports', '--clean-alluredir'])` 运行用例，自动清理并输出 allure 原始数据到 `reports/`
2. `allure generate ./reports -o ./allure_report --clean` 生成 HTML 报告到 `allure_report/`
3. `allure open ./allure_report` 自动打开报告

```bash
python run.py
```

### 2、命令行方式运行
```bash
pytest                                          # 运行全部用例
pytest cases/test_login.py                      # 运行指定文件
pytest -k "login_success"                       # 按关键字筛选
pytest --headed --slowmo=1000                   # 有头慢速运行
```

## 十、注意事项

1）首先安装本项目所需的依赖库，命令为：【pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r D:\web_auto_project\requirements.txt】，D:\web_auto_project 路径替换为你自己的项目路径即可。
2）安装 Playwright 浏览器驱动（首次必执行）：【playwright install chromium】。
3）本机需安装 Allure 命令行工具并配置环境变量，否则 `run.py` 中报告生成命令会报错。
4）环境配置，建议使用本地的 python 环境（Python 3.11），当然也可以使用虚拟环境，但是虚拟环境的第三方库版本和你本地的 python 解释器版本会有不兼容的情况，遇到哪个第三方库报错就需要卸载再重装。
5）如果运行后有报错，那就是 python 第三方库版本与本框架中的第三方库版本冲突导致，哪个报错，你就卸载哪个然后重新安装即可。
6）本项目结构下的文件，除了 `data` 目录下的测试数据文件可以自由删除，其他文件均不可以删除，否则会报错无法运行。
7）`pytest.ini` 文件名为固定写法不可更改；其中 `-p no:playwright`、`-p no:base_url` 是加载本地插件的关键配置，不可删除。
8）第三方库安装命令，使用镜像源：pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple/
9）Playwright 下拉框 `select_option()` 必须传入元素实际的 `value` 字符串值，传显示文本会导致超时等待报错。
10）依赖全局登录的用例，其 `page` fixture 需显式声明依赖 `pre_login`，否则可能在没有登录态的页面执行操作。

## 十一、Allure 测试报告环境配置

1）根目录下可自行编写 `environment.xml`（或 environment.properties）作为测试报告总览的环境显示内容，建议使用 xml 格式，因为在报告中可显示中文，.properties 格式在报告中中文会乱码。
2）里面内容可自定义编写，格式保持正确即可。
3）在执行 pytest 命令生成 allure 报告的时候，经常会加 `--clean-alluredir` 参数，其功能即是清除之前创建的 allure 测试报告原始数据（会将 `reports/` 文件夹下的文件全部清空），即此命令同样会将 environment 文件删除。
   - ①为防止 environment.properties/environment.xml 文件被删掉，可以先把该文件放在项目根目录。
   - ②执行完 run.py 第一行代码（运行用例）后。
   - ③将 environment.xml 文件再 copy 到 allure 测试报告原始数据目录（reports/）。

## 十二、Allure 测试报告常见问题

1）执行完成后，allure 测试报告没有生成：请确认本机已安装 allure 命令行工具并加入系统环境变量（`allure --version` 可验证）。
2）报告中没有用例标题/功能模块：请检查测试类和测试方法是否编写了文档字符串（框架通过文档字符串动态生成 `allure.feature` 和 `allure.title`）。
