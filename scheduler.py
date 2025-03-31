# scheduler.py
"""
定时任务调度模块，用于定期执行项目同步
"""

import time
import datetime
import schedule
from loguru import logger


def run_scheduler(job_func, interval_hours=24):
    """运行定时调度器

    Args:
        job_func: 要执行的任务函数
        interval_hours: 执行间隔（小时）

    Returns:
        None
    """
    logger.info(f"启动定时调度器，间隔: {interval_hours} 小时")
    
    # 设置定时任务
    schedule.every(interval_hours).hours.do(job_func)
    
    # 启动调度循环
    while True:
        try:
            # 检查并执行待执行的任务
            schedule.run_pending()
            
            # 记录下一次执行时间
            if schedule.jobs:
                next_run = schedule.jobs[0].next_run
                now = datetime.datetime.now()
                time_diff = next_run - now
                hours, remainder = divmod(time_diff.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                
                logger.info(f"下一次执行将在 {int(hours)} 小时 {int(minutes)} 分钟后")
            
            # 休眠一段时间
            time.sleep(60)  # 每分钟检查一次
            
        except KeyboardInterrupt:
            logger.info("收到中断信号，退出调度器")
            break
        except Exception as e:
            logger.error(f"调度器执行出错: {str(e)}")
            # 发生错误后等待恢复
            time.sleep(300)  # 5分钟后重试


def run_at_specific_time(job_func, hour=1, minute=0):
    """在每天的特定时间运行任务

    Args:
        job_func: 要执行的任务函数
        hour: 小时 (24小时制)
        minute: 分钟

    Returns:
        None
    """
    logger.info(f"启动定时调度器，将在每天 {hour:02d}:{minute:02d} 执行")
    
    # 设置在每天特定时间执行
    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(job_func)
    
    # 启动调度循环
    while True:
        try:
            schedule.run_pending()
            
            # 记录下一次执行时间
            if schedule.jobs:
                next_run = schedule.jobs[0].next_run
                now = datetime.datetime.now()
                time_diff = next_run - now
                hours, remainder = divmod(time_diff.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                
                logger.info(f"下一次执行将在 {int(hours)} 小时 {int(minutes)} 分钟后")
            
            time.sleep(60)
        except KeyboardInterrupt:
            logger.info("收到中断信号，退出调度器")
            break
        except Exception as e:
            logger.error(f"调度器执行出错: {str(e)}")
            time.sleep(300)  # 5分钟后重试


def run_with_cron_expression(job_func, cron_expression):
    """使用 cron 表达式设置定时任务

    Args:
        job_func: 要执行的任务函数
        cron_expression: cron 表达式 (例如 "0 1 * * *")

    Returns:
        None
    """
    logger.info(f"启动定时调度器，cron 表达式: {cron_expression}")
    
    # 解析 cron 表达式
    parts = cron_expression.split()
    if len(parts) != 5:
        logger.error(f"无效的 cron 表达式: {cron_expression}")
        return
    
    minute, hour, day, month, day_of_week = parts
    
    # 设置任务调度
    job = None
    
    # 处理不同的 cron 表达式情况
    # 这里只实现了部分常见的 cron 表达式转换
    # 完整实现可能需要更复杂的逻辑
    
    if minute == "0" and hour.isdigit() and day == "*" and month == "*" and day_of_week == "*":
        # 每天固定小时执行，例如 "0 1 * * *"
        job = schedule.every().day.at(f"{int(hour):02d}:00").do(job_func)
    elif minute.isdigit() and hour == "*" and day == "*" and month == "*" and day_of_week == "*":
        # 每小时固定分钟执行，例如 "30 * * * *"
        job = schedule.every().hour.at(f":{int(minute):02d}").do(job_func)
    else:
        # 默认每天执行一次
        logger.warning(f"不支持的 cron 表达式: {cron_expression}，默认为每天零点执行")
        job = schedule.every().day.at("00:00").do(job_func)
    
    # 启动调度循环
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except KeyboardInterrupt:
            logger.info("收到中断信号，退出调度器")
            break
        except Exception as e:
            logger.error(f"调度器执行出错: {str(e)}")
            time.sleep(300)
