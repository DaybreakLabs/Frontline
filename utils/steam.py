"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, visit <https://www.gnu.org/licenses/>.

Original author: TeddiO (https://github.com/TeddiO)
Modified by: DaybreakLabs (https://github.com/DaybreakLabs, dream@dreamsv.xyz)
"""
import aiohttp
import re
from urllib.parse import urlencode

class SteamSignIn:
    _host = 'https://steamcommunity.com/openid/login'

    def get_redirect(self, realm_url, response_url):
        """
        Generates the redirect URL for Steam OpenID authentication.
        """
        auth_parameters = {
            'openid.realm': realm_url,
            'openid.mode': 'checkid_setup',
            'openid.return_to': response_url,
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
        }
        return f'{self._host}?{urlencode(auth_parameters)}'

    async def validate_result(self, result):
        """
        Validates the Steam OpenID response and retrieves the user's SteamID64.
        """
        # Extract validation arguments from the OpenID result
        try:
            validation_args = {
                'openid.assoc_handle': result['openid.assoc_handle'],
                'openid.signed': result['openid.signed'],
                'openid.sig': result['openid.sig'],
                'openid.ns': result['openid.ns'],
                'openid.mode': 'check_authentication',
            }

            # Include signed arguments dynamically
            signed_args = result['openid.signed'].split(',')
            for item in signed_args:
                key = f'openid.{item}'
                if key in result:
                    validation_args[key] = result[key]
        except KeyError as e:
            raise ValueError(f"Missing required OpenID parameter: {e}")

        # Send validation request to Steam
        async with aiohttp.ClientSession() as session:
            async with session.post(self._host, data=validation_args) as response:
                response_text = await response.text()

                # Check if the response contains 'is_valid:true'
                if 'is_valid:true' in response_text:
                    # Extract SteamID64 from the claimed_id field
                    steam_id_match = re.search(
                        r'https://steamcommunity.com/openid/id/(\d+)',
                        result.get('openid.claimed_id', '')
                    )
                    if steam_id_match:
                        return steam_id_match.group(1)  # Return SteamID64
                    else:
                        raise ValueError("Unable to extract SteamID64.")
                else:
                    raise ValueError("Steam OpenID validation failed.")