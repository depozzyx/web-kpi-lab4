from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SubscriptionRequest(_message.Message):
    __slots__ = ("symbols",)
    SYMBOLS_FIELD_NUMBER: _ClassVar[int]
    symbols: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, symbols: _Optional[_Iterable[str]] = ...) -> None: ...

class TickerData(_message.Message):
    __slots__ = ("symbol", "price", "timestamp")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    price: str
    timestamp: int
    def __init__(self, symbol: _Optional[str] = ..., price: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...
