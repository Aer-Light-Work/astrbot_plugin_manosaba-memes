"""插件常量定义

此模块定义了插件中使用的所有常量，包括：
- 表情白名单
- 审判界面布局常量
- 颜色常量
"""

# 允许的表情白名单，用于防止路径遍历攻击
FACE_WHITELIST = {"害羞", "生气", "病娇", "无语", "开心"}

# 审判界面布局常量
# 图片尺寸
TRIAL_IMAGE_WIDTH = 1260
TRIAL_IMAGE_HEIGHT = 1080

# 选项框尺寸
OPTION_WIDTH = 802
OPTION_HEIGHT = 216
OPTION_START_X = 29
OPTION_START_Y = 364
OPTION_END_Y = 780

# 最大间距（像素）
MAX_PADDING = 286

# 最大选项数量限制（防止过多选项导致渲染问题）
MAX_OPTIONS_COUNT = 10

# 声明图标尺寸
STATEMENT_ICON_WIDTH = 146
STATEMENT_ICON_HEIGHT = 128
STATEMENT_OFFSET_X = 21
STATEMENT_OFFSET_Y = -43

# 文本区域偏移
TEXT_OFFSET_X = 109
TEXT_OFFSET_Y = 32
TEXT_WIDTH = 589
TEXT_HEIGHT = 150
MAX_FONT_HEIGHT = 48

# 文本颜色
TEXT_COLOR = (39, 33, 30, 255)
BRACKET_COLOR = (39, 33, 30, 255)

# 安安说话区域常量
ANAN_REGION_X = 100
ANAN_REGION_Y = 432
ANAN_REGION_WIDTH = 319
ANAN_REGION_HEIGHT = 204

# 默认字体（相对插件目录 assets/fonts/）
DEFAULT_ANAN_FONT = "assets/fonts/SourceHanSansSC-Bold.otf"
DEFAULT_TRIAL_FONT = "assets/fonts/SourceHanSerifSC.otf"

# 默认最大字号（未在设置中指定时使用；文字塞不下时自动缩小适配）
DEFAULT_ANAN_FONT_SIZE = 40
DEFAULT_TRIAL_FONT_SIZE = 48

# 安安文本中【】内的高亮颜色（紫色，保持与原版一致）
ANAN_BRACKET_COLOR = (128, 0, 128, 255)
