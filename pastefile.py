





class Booker:
    booked_dates: List[str] = [] # get_ids()
    auth, payment_id = Authenticator().get_auth_token_and_payment_method_id()

    '''create date '''
    time_delta: int = 7
    today: DT.date = DT.date.today()
    nextweek: DT.date = today + DT.timedelta(days=time_delta)
    date =  nextweek.strftime('%Y-%m-%d') # '2023-08-22'

    def keep_track_of_booked_dates(self) -> None:
        '''Adds booked to list'''
        self.booked_dates.append(self.date)

    def create_config_id(self, open_slot: dict) -> str:
        '''create config id token'''
        return open_slot['config']['token']
        
    def create_book_token(self, conf_id: str) -> str:
        '''takes params and makes book token'''
        params = (
            ('x-resy-auth-token', self.auth),
            ('config_id', conf_id),
            ('day', self.date),
            ('party_size', '2')
        )
        details_request = r.get('https://api.resy.com/3/details', headers=self.headers, params=params)
        details = details_request.json()
        return details['book_token']['value']
    
    def make_reservation(self, book_token: str) -> int:
        '''take book token and post reservation'''
        self.headers['x-resy-auth-token'] = self.auth
        data = {
        'book_token': book_token,
        'struct_payment_method': self.payment_id,
        'source_id': 'resy.com-venue-details'
        }

        response = r.post('https://api.resy.com/3/book', headers=self.headers, data=data)
        response_sc = response.status_code
        response.close()
        if response.status_code != 201:
            raise BookingError(f'There was an error and no reservation was booked. Status code: {response.status_code}')
        self.keep_track_of_booked_dates()
        return response_sc

