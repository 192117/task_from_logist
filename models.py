from pydantic import BaseModel, validator, EmailStr


class ShowTableGet(BaseModel):
    '''
        Модель для GET запросов на /show/ .
    '''

    types: str
    seats: int
    cost1: float
    cost2: float

    @validator('types')
    def check_types(cls, v):
        if v == '' or v == ' ':
            raise ValueError("It is necessary to send 'types'")
        elif v not in ['small_tables', 'medium_tables', 'big_tables']:
            raise ValueError("Incorrect 'types' ")
        else:
            return v

    @validator('seats')
    def check_seats(cls, v):
        if v == 0:
            raise ValueError("It is necessary to send 'seats'")
        elif v < 0:
            raise ValueError("It is necessary to send 'seats' > 0")
        else:
            return v

    @validator('cost1')
    def check_cost1(cls, v):
        if v == float(0):
            raise ValueError("It is necessary to send 'cost1'")
        elif v < 0:
            raise ValueError("It is necessary to send 'cost1' > 0")
        else:
            return v

    @validator('cost2')
    def check_cost2(cls, v):
        if v == float(0):
            raise ValueError("It is necessary to send 'cost2'")
        elif v < 0:
            raise ValueError("It is necessary to send 'cost2' > 0")
        else:
            return v


class OrderPost(BaseModel):
    '''
        Модель для POST запросов на /order/ .
    '''

    id: int
    types: str
    mail: EmailStr

    @validator('id')
    def check_id(cls, v):
        if v == 0:
            raise ValueError("It is necessary to send 'id'")
        elif v < 0:
            raise ValueError("It is necessary to send 'id' > 0")
        else:
            return v

    @validator('types')
    def check_types(cls, v):
        if v == '':
            raise ValueError("It is necessary to send 'types'")
        else:
            return v


class UserRegistrModelPost(BaseModel):
    '''
        Модель для POST запросов на /registr/ .
    '''

    username: str
    password1: str
    password2: str

    @validator('username')
    def check_username(cls, v):
        if v == '':
            raise ValueError("It is necessary to send 'username'")
        else:
            return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v


class UserLoginModelPost(BaseModel):
    '''
        Модель для POST запросов на /login/ .
    '''

    username: str
    password: str

    @validator('username')
    def check_username(cls, v):
        if v == '':
            raise ValueError("It is necessary to send 'username'")
        else:
            return v

    @validator('password')
    def check_password(cls, v):
        if len(v) == 0:
            raise ValueError("It is necessary to send 'password'")
        else:
            return v


class UserCloseModelPost(BaseModel):
    '''
        Модель для POST запросов на /close/ .
    '''

    types: str
    id: int

    @validator('types')
    def check_types(cls, v):
        if v == '' or v == ' ':
            raise ValueError("It is necessary to send 'types'")
        elif v not in ['small_tables', 'medium_tables', 'big_tables']:
            raise ValueError("Incorrect 'types' ")
        else:
            return v

    @validator('id')
    def check_id(cls, v):
        if v == 0:
            raise ValueError("It is necessary to send 'id'")
        elif v < 0:
            raise ValueError("It is necessary to send 'id' > 0")
        else:
            return v


class UserChangePriceModelPost(BaseModel):
    '''
        Модель для POST запросов на /change_price/ .
    '''

    types: str
    id: int
    cost: float

    @validator('types')
    def check_types(cls, v):
        if v == '' or v == ' ':
            raise ValueError("It is necessary to send 'types'")
        elif v not in ['small_tables', 'medium_tables', 'big_tables']:
            raise ValueError("Incorrect 'types' ")
        else:
            return v

    @validator('id')
    def check_id(cls, v):
        if v == 0:
            raise ValueError("It is necessary to send 'id'")
        elif v < 0:
            raise ValueError("It is necessary to send 'id' > 0")
        else:
            return v

    @validator('cost')
    def check_cost(cls, v):
        if v == float(0):
            raise ValueError("It is necessary to send 'cost'")
        elif v < 0:
            raise ValueError("It is necessary to send 'cost' > 0")
        else:
            return v


class UserAddModelPost(BaseModel):
    '''
        Модель для POST запросов на /add_tables/ .
    '''

    types: str
    count: int
    seats: int
    cost: float

    @validator('types')
    def check_types(cls, v):
        if v == '' or v == ' ':
            raise ValueError("It is necessary to send 'types'")
        elif v not in ['small_tables', 'medium_tables', 'big_tables']:
            raise ValueError("Incorrect 'types' ")
        else:
            return v

    @validator('count')
    def check_count(cls, v):
        if v == 0:
            raise ValueError("It is necessary to send 'count'")
        elif v < 0:
            raise ValueError("It is necessary to send 'count' > 0")
        else:
            return v

    @validator('seats')
    def check_seats(cls, v):
        if v == 0:
            raise ValueError("It is necessary to send 'seats'")
        elif v < 0:
            raise ValueError("It is necessary to send 'seats' > 0")
        else:
            return v

    @validator('cost')
    def check_cost(cls, v):
        if v == float(0):
            raise ValueError("It is necessary to send 'cost'")
        elif v < 0:
            raise ValueError("It is necessary to send 'cost' > 0")
        else:
            return v


class UserChangeTableModelPost(BaseModel):
    '''
        Модель для POST запросов на /change_table/ .
    '''

    types: str
    id: int
    seats: int
    cost: float

    @validator('types')
    def check_types(cls, v):
        if v == '' or v == ' ':
            raise ValueError("It is necessary to send 'types'")
        elif v not in ['small_tables', 'medium_tables', 'big_tables']:
            raise ValueError("Incorrect 'types' ")
        else:
            return v

    @validator('id')
    def check_id(cls, v):
        if v == 0:
            raise ValueError("It is necessary to send 'id'")
        elif v < 0:
            raise ValueError("It is necessary to send 'id' > 0")
        else:
            return v

    @validator('seats')
    def check_seats(cls, v):
        if v == 0:
            raise ValueError("It is necessary to send 'seats'")
        elif v < 0:
            raise ValueError("It is necessary to send 'seats' > 0")
        else:
            return v

    @validator('cost')
    def check_cost(cls, v):
        if v == float(0):
            raise ValueError("It is necessary to send 'cost'")
        elif v < 0:
            raise ValueError("It is necessary to send 'cost' > 0")
        else:
            return v


class UserBookingPost(BaseModel):
    '''
        Модель для POST запросов на /booking/ .
    '''

    types: str
    id: int
    booking: bool

    @validator('types')
    def check_types(cls, v):
        if v == '' or v == ' ':
            raise ValueError("It is necessary to send 'types'")
        elif v not in ['small_tables', 'medium_tables', 'big_tables']:
            raise ValueError("Incorrect 'types ")
        else:
            return v

    @validator('id')
    def check_id(cls, v):
        if v == 0:
            raise ValueError("It is necessary to send 'id'")
        elif v < 0:
            raise ValueError("It is necessary to send 'id' > 0")
        else:
            return v

    @validator('booking')
    def check_booking(cls, v):
        if isinstance(v, bool):
            return v
        else:
            raise ValueError("It is not boolean")




