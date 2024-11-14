import asyncio
from pyppeteer import launch
import time


# 定义协程
async def Summary_all(Sumary_all, pasword, username):
    # 启动浏览器
    browser = await launch(headless=True)  # headless=False 可以看到浏览器界面
    page = await browser.newPage()

    # 导航到登录页面
    await page.screenshot({'path': 'login_success.png'})
    await page.goto(Sumary_all)
    await page.screenshot({'path': 'login_success.png'})

    await page.waitForSelector('div[class="switch-login-mode-box"]')
    await page.click('div[class="switch-login-mode-box"]')
    await page.screenshot({'path': 'login_success.png'})

    # 等待用户名输入框
    await page.waitForSelector('input[class="ud__checkbox__input"]')
    await page.screenshot({'path': 'login_success.png'})

    # 勾选同意
    await page.click('input[class="ud__checkbox__input"]')
    await page.screenshot({'path': 'login_success.png'})
    # 下一步
    await page.click(
        'button[class="ud__button ud__button--outlined ud__button--outlined-default ud__button--round ud__button--size-lg sso-login-sso-button _pp-ud-btn-inline-block"]')
    await page.screenshot({'path': 'login_success.png'})
    # 填写企业域名
    await page.waitForSelector('input[class="ud__native-input"]')

    await page.type('input[class="ud__native-input"]', 'nio')
    await page.screenshot({'path': 'login_success.png'})
    # 下一步
    await page.click(
        'button[class="ud__button ud__button--filled ud__button--filled-default ud__button--size-lg ud__button--block _pp-ud-btn-block"]')

    await page.screenshot({'path': 'login_success.png'})

    # 等待输入框
    await page.waitForSelector('input[id="username"]')
    await page.screenshot({'path': 'login_success.png'})

    # 填写账号密码
    await page.type('input[id="username"]', username)
    await page.type('input[id="pwd"]', pasword)
    await page.screenshot({'path': 'login_success.png'})

    # 点击登录按钮
    time.sleep(2)
    await page.waitForSelector('button[class="btn login-btn cn"]')
    await page.screenshot({'path': 'login_success.png'})
    await page.click('button[class="btn login-btn cn"]')  # 根据实际情况调整选择器

    time.sleep(15)
    # 截图
    await page.setViewport({'width': 1920, 'height': 1080})
    # await page.screenshot(path="screenshot.png", full_page=True)
    await page.screenshot(path="summary_all.png", clip={'x': 250, 'y': 195, 'width': 1250, 'height': 250})

    await browser.close()


# 定义协程
async def Summary(Sumary, pasword, username):
    # 启动浏览器
    browser = await launch(headless=True)  # headless=False 可以看到浏览器界面
    page = await browser.newPage()

    # 导航到登录页面
    await page.screenshot({'path': 'login_success.png'})
    await page.goto(Sumary)
    await page.screenshot({'path': 'login_success.png'})

    await page.waitForSelector('div[class="switch-login-mode-box"]')
    await page.click('div[class="switch-login-mode-box"]')
    await page.screenshot({'path': 'login_success.png'})

    # 等待用户名输入框
    await page.waitForSelector('input[class="ud__checkbox__input"]')
    await page.screenshot({'path': 'login_success.png'})

    # 勾选同意
    await page.click('input[class="ud__checkbox__input"]')
    await page.screenshot({'path': 'login_success.png'})
    # 下一步
    await page.click(
        'button[class="ud__button ud__button--outlined ud__button--outlined-default ud__button--round ud__button--size-lg sso-login-sso-button _pp-ud-btn-inline-block"]')
    await page.screenshot({'path': 'login_success.png'})
    # 填写企业域名
    await page.waitForSelector('input[class="ud__native-input"]')

    await page.type('input[class="ud__native-input"]', 'nio')
    await page.screenshot({'path': 'login_success.png'})
    # 下一步
    await page.click(
        'button[class="ud__button ud__button--filled ud__button--filled-default ud__button--size-lg ud__button--block _pp-ud-btn-block"]')

    await page.screenshot({'path': 'login_success.png'})

    # 等待输入框
    await page.waitForSelector('input[id="username"]')
    await page.screenshot({'path': 'login_success.png'})

    # 填写账号密码
    await page.type('input[id="username"]', username)
    await page.type('input[id="pwd"]', pasword)
    await page.screenshot({'path': 'login_success.png'})

    # 点击登录按钮
    time.sleep(2)
    await page.waitForSelector('button[class="btn login-btn cn"]')
    await page.screenshot({'path': 'login_success.png'})
    await page.click('button[class="btn login-btn cn"]')  # 根据实际情况调整选择器

    time.sleep(15)
    # 截图
    await page.setViewport({'width': 3000, 'height': 2000})
    await page.screenshot(path="screenshot.png", full_page=True)
    await page.screenshot(path="summary_rc.png", clip={'x': 50, 'y': 200, 'width': 2300, 'height': 1500})

    await browser.close()


# 运行主函数
Sumary = 'https://nio.feishu.cn/base/YqcGbCa62armnmsEDUScH7tinvg?table=tbliRBqcNer6xpZc'
Sumary_all = 'https://nio.feishu.cn/base/PWoIbkYvOarcpDs4jmEc4Q4xnZd?table=tblC2gLpuJeq9TmS'  # 报告链接  前面这俩是报告的链接
username = 'zhenkai.shen.o'
pasword = 'Szk990202@yxy'

# 启动两个协程
asyncio.get_event_loop().run_until_complete(Summary_all(Sumary_all, pasword, username))
asyncio.get_event_loop().run_until_complete(Summary(Sumary, pasword, username))





