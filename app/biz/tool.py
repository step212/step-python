from agents import function_tool

@function_tool
async def do_some_work(work_name: str) -> str:
    """
    Do some work/做一些工作
    Args:
        work_name: The name of the work to do/要做的工作的名称
    Returns:
        A string indicating that the work is done/一个字符串，表示工作已经完成
    """
    print(f"do_some_work: {work_name}")
    return "done"





