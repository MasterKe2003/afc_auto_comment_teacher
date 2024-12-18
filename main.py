import random
from selenium import webdriver  
from selenium.webdriver.common.by import By
import time

username = ''
password = ''
# 创建WebDriver实例，这里以Chrome为例  
driver = webdriver.Chrome()  

# 登录办事大厅
driver.get('https://authserver.afc.edu.cn/authserver/login')  # 替换为你要操作的网页地址  
driver.implicitly_wait(10)  
driver.find_element(By.ID, 'username').send_keys(username)
password_input = driver.find_element(By.ID, 'password')  
driver.execute_script("arguments[0].removeAttribute('readonly')", password_input)  
password_input.send_keys(password)
driver.find_element(By.ID, 'login_submit').click()
time.sleep(1)

# 进入教务系统
driver.get('https://ehall.afc.edu.cn/appShow?appId=5711907003536952')
driver.implicitly_wait(10)  
driver.find_element(By.LINK_TEXT, '教学评价').click()
driver.find_element(By.LINK_TEXT, '学生评价').click()
original_window = driver.current_window_handle
all_windows = driver.window_handles
for window in all_windows:
    if window != original_window:
        driver.switch_to.window(window)
        break

while True:
    try:
        # 每次都重新查找 "未评" 元素
        elements = driver.find_elements(By.XPATH, '//td[@title="未评"]')
        time.sleep(3)
        # 遍历所有找到的 "未评" 元素
        elements[0].click()
        time.sleep(3)
        
        # 获取当前页面中所有 class="tr-xspj" 的元素
        scores = driver.find_elements(By.CLASS_NAME, 'tr-xspj')
        
        # 为每个 score 元素输入一个随机分数
        for score in scores:
            # 生成 90 到 100 之间的随机分数
            random_score = random.randint(95, 100)
            
            # 定位到当前 tr-xspj 元素下的 input 元素
            input_field = score.find_element(By.CLASS_NAME, 'form-control')
            
            # 清空输入框并输入随机分数
            input_field.clear()
            input_field.send_keys(str(random_score))  # 输入随机分数
            time.sleep(1)
        
        # 提交评分并确认
        time.sleep(3)
        driver.find_element(By.ID, 'btn_xspj_tj').click()
        time.sleep(3)
        # try:
        #     driver.find_element(By.ID, 'btn_confirm').click()  # 确认按钮
        #     time.sleep(2)
        # except:  # 如果按钮不可用，则跳过
        #     pass
        driver.find_element(By.ID, 'btn_ok').click()  # 确认按钮
        time.sleep(3)
        # 如果没有更多的 "未评" 元素，退出循环
        if not elements:
            print("没有更多未评元素，退出循环。")
            break

    except Exception as e:
        print(f"发生了错误：{str(e)}")
        break  # 出现错误时退出循环

# 关闭浏览器
driver.quit()
