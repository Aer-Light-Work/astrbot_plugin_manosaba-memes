import sys
from pathlib import Path
from typing import Optional, List, Tuple

from sketchbook import (  # type: ignore
    Drawer,
    TextStyle,
    Region,
    Layer,
    ScaleMode,
    FontSet,
)

try:
    from sketchbook import ParseRule  # type: ignore
    _PARSE_RULE_AVAILABLE = True
except ImportError:  # 部分环境/版本的 sketchbook 未导出 ParseRule
    ParseRule = None  # type: ignore
    _PARSE_RULE_AVAILABLE = False

from .models import Character, Option, Statement
from .constants import (
    FACE_WHITELIST,
    TRIAL_IMAGE_WIDTH,
    TRIAL_IMAGE_HEIGHT,
    OPTION_WIDTH,
    OPTION_HEIGHT,
    OPTION_START_X,
    OPTION_START_Y,
    OPTION_END_Y,
    MAX_OPTIONS_COUNT,
    STATEMENT_ICON_WIDTH,
    STATEMENT_ICON_HEIGHT,
    STATEMENT_OFFSET_X,
    STATEMENT_OFFSET_Y,
    TEXT_OFFSET_X,
    TEXT_OFFSET_Y,
    TEXT_WIDTH,
    TEXT_HEIGHT,
    TEXT_COLOR,
    BRACKET_COLOR,
    ANAN_REGION_X,
    ANAN_REGION_Y,
    ANAN_REGION_WIDTH,
    ANAN_REGION_HEIGHT,
    DEFAULT_ANAN_FONT,
    DEFAULT_TRIAL_FONT,
    DEFAULT_ANAN_FONT_SIZE,
    DEFAULT_TRIAL_FONT_SIZE,
    ANAN_BRACKET_COLOR,
)


PLUGIN_PATH = Path(__file__).parent


def _resolve_font(value: Optional[str], default_rel: str) -> str:
    """解析字体路径。

    优先使用用户配置的路径（绝对路径，或相对于插件目录的路径）；
    若不存在或为空则回退到随插件附带的默认字体。

    Args:
        value (Optional[str]): 用户配置的字体路径（`.ttf` / `.otf`）
        default_rel (str): 插件内默认字体的相对路径

    Returns:
        str: 可用的字体文件绝对路径
    """
    if value:
        raw = Path(value).expanduser()
        if raw.is_file():
            return str(raw)
        relative = PLUGIN_PATH / raw
        if relative.is_file():
            return str(relative)
        print(
            f"[manosaba-memes] 警告: 自定义字体路径无效，已回退默认字体: {value}",
            file=sys.stderr,
        )
    return str(PLUGIN_PATH / default_rel)


def _make_font_set(primary: str, default_rel: str) -> FontSet:
    """创建字体集合。

    自定义字体在前、默认字体在后，构成回退链：
    即使自定义字体缺少某些字形，也会自动用默认字体补齐，不会中断渲染。

    Args:
        primary (str): 主字体路径（可能来自用户配置）
        default_rel (str): 默认字体相对路径（回退字体）

    Returns:
        FontSet: 配置好回退链的字体集合
    """
    default_path = str(PLUGIN_PATH / default_rel)
    fonts = FontSet(primary)
    if primary != default_path:
        fonts.add(default_path)
    return fonts


def get_anan_base_image(face: Optional[str] = None) -> str:
    """Get the base image path for Anan's face

    Args:
        face (Optional[str], optional): The face type to be used. 
                                       Available: 害羞, 生气, 病娇, 无语, 开心. 
                                       Defaults to None.

    Returns:
        str: The path to the base image
        
    Raises:
        ValueError: If face is not in the whitelist
    """
    if face is None:
        return str(PLUGIN_PATH / "assets/anan/base.png")
    
    # 安全校验：确保 face 在白名单中，防止路径遍历攻击
    if face not in FACE_WHITELIST:
        raise ValueError(f"Invalid face type: {face}. Must be one of {FACE_WHITELIST}")
    
    # 使用 .name 获取文件名部分，确保路径不会包含目录分隔符
    safe_face = Path(face).name
    return str(PLUGIN_PATH / "assets/anan" / f"{safe_face}.png")


def draw_anan(
    text: str,
    face: Optional[str] = None,
    font: Optional[str] = None,
    max_font_size: Optional[float] = None,
) -> bytes:
    """Draw the image of what Anan says

    Args:
        text (str): The text to be drawn
        face (Optional[str], optional): The face type to be used. 
                                       Available: 害羞, 生气, 病娇, 无语, 开心. 
                                       Defaults to None.
        font (Optional[str], optional): Custom font path. Defaults to None (use bundled font).
        max_font_size (Optional[float], optional): Maximum font size in px. 
                                                  None means auto-fit to the region.

    Returns:
        bytes: The image bytes of the drawn image
    """
    primary_font = _resolve_font(font, DEFAULT_ANAN_FONT)
    fonts = _make_font_set(primary_font, DEFAULT_ANAN_FONT)

    drawer = Drawer.from_image(get_anan_base_image(face), fonts)
    drawer.overlay(str(PLUGIN_PATH / "assets/anan/base_overlay.png"))

    # 未指定字号时使用默认字号（文字塞不下时自动缩小适配）
    effective_max_font_size = (
        float(max_font_size)
        if max_font_size is not None
        else float(DEFAULT_ANAN_FONT_SIZE)
    )

    region = Region(ANAN_REGION_X, ANAN_REGION_Y, ANAN_REGION_WIDTH, ANAN_REGION_HEIGHT)
    style_kwargs = {
        "color": (0, 0, 0, 255),
        "max_font_size": effective_max_font_size,
    }
    if _PARSE_RULE_AVAILABLE:
        style_kwargs["parse_rules"] = [ParseRule.cn_bracket(ANAN_BRACKET_COLOR)]
    drawer.layer(Layer("text").text(text, region, TextStyle(**style_kwargs)))
    return drawer.render()


def get_statement_image(statement: Statement) -> str:
    """Get the image path for a statement type

    Args:
        statement (Statement): The statement type

    Returns:
        str: The path to the statement image
        
    Raises:
        ValueError: If statement type is not recognized
    """
    mapping = {
        Statement.AGREEMENT: "agreement.png",
        Statement.DOUBT: "doubt.png",
        Statement.PERJURY: "perjury.png",
        Statement.REFUTATION: "refutation.png",
        Statement.MAGIC_CHIYUSAISEI: "magic_chiyusaisei.png",
        Statement.MAGIC_EKITAISOUSA: "magic_ekitaisousa.png",
        Statement.MAGIC_FUYUU: "magic_fuyuu.png",
        Statement.MAGIC_GENSHI: "magic_genshi.png",
        Statement.MAGIC_HAKKA: "magic_hakka.png",
        Statement.MAGIC_IREKAWARI: "magic_irekawari.png",
        Statement.MAGIC_KAIRIKI: "magic_kairiki.png",
        Statement.MAGIC_MAJOGOROSHI: "magic_majogoroshi.png",
        Statement.MAGIC_MONOMANE: "magic_monomane.png",
        Statement.MAGIC_SENNOU: "magic_sennou.png",
        Statement.MAGIC_SENRIGAN: "magic_senrigan.png",
        Statement.MAGIC_SHINIMODORI: "magic_shinimodori.png",
        Statement.MAGIC_SHISENYUUDOU: "magic_shisenyuudou.png",
    }
    
    # 使用 .get() 方法，避免直接索引可能引发的 KeyError
    image_file = mapping.get(statement)
    if image_file is None:
        raise ValueError(f"未知的陈述类型: {statement}")
    
    return str(PLUGIN_PATH / "assets/trial" / image_file)


def get_option_coordinates(number: int) -> List[Tuple[int, int]]:
    """Get the coordinates for drawing options based on the number of options
    
    布局算法说明：
    - 选项在审判界面中从上到下排列
    - 确保选项之间至少有 20px 的间距，避免挤在一起
    - 在可用范围内垂直居中显示所有选项
    
    Args:
        number (int): The number of options

    Returns:
        List[Tuple[int, int]]: A list of (x, y) coordinates for each option
        
    Raises:
        ValueError: If number of options exceeds the maximum limit
    """
    # 前置校验：确保选项数量在合理范围内
    if number > MAX_OPTIONS_COUNT:
        raise ValueError(f"选项数量过多，最多支持 {MAX_OPTIONS_COUNT} 个选项")
    
    if number <= 0:
        raise ValueError("选项数量必须大于 0")
    
    # 最小间距（确保选项不会挤在一起）
    MIN_SPACING = 20
    
    # 计算所需的总高度（选项高度 + 最小间距）
    total_layout_height = number * OPTION_HEIGHT + (number - 1) * MIN_SPACING
    
    # 计算可用高度
    available_height = OPTION_END_Y - OPTION_START_Y
    
    if number == 1:
        # 单个选项，垂直居中
        start_y = OPTION_START_Y + (available_height - OPTION_HEIGHT) // 2
        return [(OPTION_START_X, start_y)]
    
    # 计算起始Y坐标，使整体布局垂直居中
    # 如果总高度超过可用高度，从 OPTION_START_Y 开始
    if total_layout_height > available_height:
        start_y = OPTION_START_Y
    else:
        start_y = OPTION_START_Y + (available_height - total_layout_height) // 2
    
    # 生成选项坐标，每个选项之间保持 MIN_SPACING 间距
    return [
        (OPTION_START_X, start_y + i * (OPTION_HEIGHT + MIN_SPACING))
        for i in range(number)
    ]


def draw_trial(
    character: Character,
    options: List[Option],
    font: Optional[str] = None,
    max_font_size: Optional[float] = None,
) -> bytes:
    """Draw the trial image for a character saying an option

    Args:
        character (Character): The character who is speaking
        options (List[Option]): The options being spoken
        font (Optional[str], optional): Custom font path. Defaults to None (use bundled font).
        max_font_size (Optional[float], optional): Maximum font size in px.
                                                  None uses the default 48.

    Returns:
        bytes: The image bytes of the drawn image
        
    Raises:
        ValueError: If options count exceeds maximum limit
    """
    # 前置校验：确保选项数量在合理范围内
    if len(options) > MAX_OPTIONS_COUNT:
        raise ValueError(f"选项数量过多，最多支持 {MAX_OPTIONS_COUNT} 个选项")
    
    if len(options) == 0:
        raise ValueError("选项数量不能为 0")

    primary_font = _resolve_font(font, DEFAULT_TRIAL_FONT)
    fonts = _make_font_set(primary_font, DEFAULT_TRIAL_FONT)

    # 画布与角色层
    drawer = Drawer(TRIAL_IMAGE_WIDTH, TRIAL_IMAGE_HEIGHT, fonts)
    drawer.layer(
        Layer("background").image_fit(
            str(PLUGIN_PATH / "assets/trial/background.png"),
            drawer.full_region(),
            scale=ScaleMode.Stretch,
        )
    )
    drawer.layer(
        Layer("character").image_fit(
            str(
                PLUGIN_PATH
                / "assets/trial"
                / ("ema.png" if character == Character.EMA else "hiro.png")
            ),
            Region(667, 0, TRIAL_IMAGE_WIDTH - 667, TRIAL_IMAGE_HEIGHT),
            scale=ScaleMode.Stretch,
        )
    )

    # 实际使用的最大字号（None -> 默认值 48）
    effective_max_font_size = (
        float(max_font_size)
        if max_font_size is not None
        else float(DEFAULT_TRIAL_FONT_SIZE)
    )

    # Options, texts, and statements
    coordinates = get_option_coordinates(len(options))
    for i, (option, (x, y)) in enumerate(zip(options, coordinates)):
        # 选项背景框
        drawer.layer(
            Layer(f"option_bg_{i}").image_fit(
                str(PLUGIN_PATH / "assets/trial/option.png"),
                Region(x, y, OPTION_WIDTH, OPTION_HEIGHT),
                scale=ScaleMode.Stretch,
            )
        )
        # 选项文本（【】高亮，字号自适应区域，上限 effective_max_font_size）
        style_kwargs = {
            "color": TEXT_COLOR,
            "max_font_size": effective_max_font_size,
        }
        if _PARSE_RULE_AVAILABLE:
            style_kwargs["parse_rules"] = [ParseRule.cn_bracket(BRACKET_COLOR)]
        drawer.layer(
            Layer(f"option_text_{i}").text(
                option.text,
                Region(
                    x + TEXT_OFFSET_X,
                    y + TEXT_OFFSET_Y,
                    TEXT_WIDTH,
                    TEXT_HEIGHT,
                ),
                TextStyle(**style_kwargs),
            )
        )
        # 陈述类型图标（保持比例适配）
        drawer.layer(
            Layer(f"option_stmt_{i}").image_fit(
                get_statement_image(option.statement),
                Region(
                    x + STATEMENT_OFFSET_X,
                    y + STATEMENT_OFFSET_Y,
                    STATEMENT_ICON_WIDTH,
                    STATEMENT_ICON_HEIGHT,
                ),
                scale=ScaleMode.Fit,
            )
        )

    return drawer.render()
