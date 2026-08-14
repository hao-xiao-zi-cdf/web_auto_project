import json

"""
/**** 模拟新增项目 返回 400  ***/
"""
mock_project_400 = {
    "url": "**/api/project",
    "handler": lambda route: route.fulfill(
        status=400,
        body=json.dumps({
            "errors":
                {
                    "project_name": "yo yo 已存在"
                },
            "message": "Input payload validation failed"
        })
    )
}

"""
/**** 模拟新增项目 返回 500  ***/
"""
mock_project_500 = {
    "url": "**/api/project",
    "handler": lambda route: route.fulfill(
        status=500,
        body="服务端错误"
    )
}

"""
/**** 模拟新增项目 返回 200  ***/
"""
mock_project_200 = {
    "url": "**/api/project",
    "handler": lambda route: route.fulfill(
        status=200,
        body='{"code": 0, "message": "success", "data": {}}'
    )
}

"""
/**** 模拟项目列表 搜索结果 0 条 ***/
"""
mock_project_search_0 = {
    "url": "**/api/project**",
    "handler": lambda route: route.fulfill(
        status=200,
        body=json.dumps({
            "total": 0,
            "rows": []
        })
    )
}

"""
/**** 模拟项目列表 搜索结果 1 条 ***/
"""
mock_project_search_1 = {
    "url": "**/api/project**",
    "handler": lambda route: route.fulfill(
        status=200,
        body=json.dumps({
            "total": 1,
            "rows": [
                {
                    "id": 1,
                    "project_name": "testzz",
                    "publish_app": "",
                    "project_desc": "",
                    "active": "1",
                    "create_time": "2023-02-17 11:59:33",
                    "update_time": "2023-02-17 11:59:33",
                    "test_user": "py"}
            ]
        })
    )
}

"""
/**** 模拟项目列表 删除返回403 无权限 ***/
"""
mock_project_delete_403 = {
    "url": "**/api/project**",
    "handler": lambda route: route.fulfill(
        status=403,
        body=json.dumps({"message": "无权限操作，请联系管理员"})
    )
}

"""
/**** 模拟新增模块 项目选项 ***/
"""
mock_project_select_200 = {
    "url": "**/api/project",
    "handler": lambda route: route.fulfill(
        status=200,
        body=json.dumps({
            "total": 9,
            "rows": [
                {
                    "id": 53,
                    "project_name": "test",
                    "publish_app": "",
                    "project_desc": "",
                    "active": "1",
                    "create_time": "2023-03-02 11:30:00",
                    "update_time": "2023-03-02 11:30:00",
                    "test_user": "py"
                },
                {
                    "id": 43,
                    "project_name": "hello",
                    "publish_app": "xx",
                    "project_desc": "xxx",
                    "active": "1",
                    "create_time": "2023-03-01 22:06:05",
                    "update_time": "2023-03-01 22:06:05",
                    "test_user": "py"
                }, {
                    "id": 42,
                    "project_name": "world",
                    "publish_app": "xx",
                    "project_desc": "xxx",
                    "active": "1",
                    "create_time": "2023-03-01 21:30:06",
                    "update_time": "2023-03-01 21:30:06",
                    "test_user": "py"
                }, {
                    "id": 41,
                    "project_name": "测试项目",
                    "publish_app": "xx",
                    "project_desc": "xxx",
                    "active": "1",
                    "create_time": "2023-03-01 21:29:35",
                    "update_time": "2023-03-01 21:29:35",
                    "test_user": "py"
                }]
        })
    )
}

"""
/**** 模拟新增模块，模块名称重复，返回400  ***/
"""
mock_add_module_400 = {
    "url": "**/api/module",
    "handler": lambda route: route.fulfill(
        status=400,
        body=json.dumps({"message": "module_name: test 已存在"})
    )
}

"""
/**** 模拟新增模块，添加成功，返回200  ***/
"""
mock_add_module_200 = {
    "url": "**/api/module",
    "handler": lambda route: route.fulfill(
        status=200,
        body=json.dumps({"code": 0, "message": "success", "data": {}})
    )
}

"""
/**** 模拟新增环境，环境名称已存在，返回400  ***/
"""
mock_add_env_400 = {
    "url": "**/api/env",
    "handler": lambda route: route.fulfill(
        status=400,
        body=json.dumps({
            "errors": {"env_name": "env_name: py1 已存在"},
            "message": "Input payload validation failed"
        })
    )
}

"""
/**** 模拟新增环境，成功，返回200  ***/
"""
mock_add_env_200 = {
    "url": "**/api/env",
    "handler": lambda route: route.fulfill(
        status=200,
        body=json.dumps({"code": 0, "message": "success", 'data': {}})
    )
}
