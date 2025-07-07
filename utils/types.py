try:
    from typing import TypedDict, Literal, NotRequired, Union
except ImportError:
    # Python < 3.11 兼容性
    from typing import TypedDict, Literal, Union
    try:
        from typing_extensions import NotRequired
    except ImportError:
        # 如果没有typing_extensions，定义一个简单的NotRequired
        def NotRequired(tp):
            return tp

OriginType = Literal["live", "hls", "local", "whitelist", "subscribe", "hotel", "multicast", "online_search"]
IPvType = Literal["ipv4", "ipv6", None]


class ChannelData(TypedDict):
    """
    Channel data types, including url, date, resolution, origin and ipv_type
    """
    id: int
    url: str
    host: str
    date: NotRequired[Union[str, None]]
    resolution: NotRequired[Union[str, None]]
    origin: OriginType
    ipv_type: IPvType
    location: NotRequired[Union[str, None]]
    isp: NotRequired[Union[str, None]]
    headers: NotRequired[Union[dict[str, str], None]]
    catchup: NotRequired[Union[dict[str, str], None]]
    extra_info: NotRequired[str]


CategoryChannelData = dict[str, dict[str, list[ChannelData]]]


class TestResult(TypedDict):
    """
    Test result types, including speed, delay, resolution
    """
    speed: Union[int, float, None]
    delay: Union[int, float, None]
    resolution: Union[int, str, None]


TestResultCacheData = dict[str, list[TestResult]]

ChannelTestResult = Union[ChannelData, TestResult]
