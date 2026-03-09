import datetime
import os
from typing import Optional, Dict, Any, List

import requests

from src.texioty.helpers.apis.api_helper import BaseAPIHelper


class ImmutableAPI(BaseAPIHelper):
    def __init__(self, environment: str = 'sandbox', chain_name: str = 'imtbl-zkevm-testnet'):
        """
        Initializes the Immutable API helper with specified environment and chain name.

        Args:
            environment (str): The environment to use for API calls ('sandbox' or 'production').
            chain_name (str): The name of the blockchain network to interact with ('imtbl-zkevm-testnet' or 'imtbl-zkevm-mainnet').
        """
        super().__init__()
        self.environment = environment
        self.chain_name = chain_name
        if environment == 'sandbox':
            self.base_url = 'https://api.sandbox.immutable.com'
        else:
            self.base_url = 'https://api.immutable.com'

        self.headers = {'Content-Type': 'application/json'}
        if api_key := os.getenv('IMX_API_KEY'):
            self.headers['Authorization'] = f'Bearer {api_key}'

    def endpoint_builder(self, endpoint_path: str, params: Optional[Dict[str, Any]] = None) -> str:
        endpoint = f'{self.base_url}{endpoint_path}'
        self.previous_endpoint = endpoint
        return endpoint

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None, debug=False) -> Dict[str, Any]:
        """
        Make HTTP GET request to the specified endpoint.
        Args:
            endpoint: Full endpoint URL.
            params: query parameters
        Returns:
            Response JSON as dictionary.
        """
        try:
            if debug:
                print(f"Making request to {endpoint}\n with params {params}\n using headers {self.headers}")
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            if debug:
                print(f"Status code: {response.status_code}")
                print(f"Response: {response.text[:500]}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return {}

    def get_token_prices(self, contract_addresses: List[str]) -> Dict[str, Any]:
        """
        Fetch token prices and details.
        Args:
            contract_addresses: List of token contract addresses.
        Returns:
            Dictionary with token prices and details.
        """
        endpoint = self.endpoint_builder(f'/v1/chains/{self.chain_name}/tokens')
        tokens_data = {}

        for address in contract_addresses:
            params = {'contract_address': address}
            token_data = self._make_request(endpoint, params)
            if token_data and 'result' in token_data:
                tokens_data[address] = token_data['result'][0] if token_data['result'] else {}
        return tokens_data

    def get_wallet_nfts(self, wallet_address: str, page_size: int = 100, page_cursor: Optional[str] = None) -> Dict[str, Any]:
        endpoint = self.endpoint_builder(f'/v1/chains/{self.chain_name}/accounts/{wallet_address}/nft-balances')
        params = {'page_size': min(page_size, 200)}
        if page_cursor:
            params['page_cursor'] = page_cursor
        return self._make_request(endpoint, params)

    def get_wallet_token_balances(self, wallet_address: str) -> Dict[str, Any]:
        endpoint = self.endpoint_builder(f'/v1/chains/{self.chain_name}/accounts/{wallet_address}')
        return self._make_request(endpoint)

    def get_activity_history(self,
                             from_updated_at: datetime.datetime,
                             to_updated_at: Optional[datetime.datetime] = None,
                             contract_address: Optional[str] = None,
                             activity_type: Optional[str] = None,
                             page_size: int = 100,
                             page_cursor: Optional[str] = None
                             ) -> Dict[str, Any]:
        endpoint = self.endpoint_builder(f'/v1/chains/{self.chain_name}/activity-history')
        from_time = from_updated_at.isoformat()
        if not from_time.endswith('Z'):
            from_time += 'Z'
        params = {
            'from_updated_at': from_time,
            'page_size': min(page_size, 200)}
        if to_updated_at:
            to_time = to_updated_at.isoformat()
            if not to_time.endswith('Z'):
                to_time += 'Z'
            params['to_updated_at'] = to_time
        if contract_address:
            params['contract_address'] = contract_address
        if activity_type:
            params['activity_type'] = activity_type
        if page_cursor:
            params['page_cursor'] = page_cursor
        return self._make_request(endpoint, params)

    def get_wallet_transfers(self, wallet_address: str, hours_back: int = 24) -> Dict[str, Any]:
        to_time = datetime.datetime.utcnow()
        from_time = to_time - datetime.timedelta(hours=hours_back)
        transfers = self.get_activity_history(from_time, to_time, activity_type='transfer')
        return transfers

    def get_wallet_portfolio_value(self, wallet_address: str) -> Dict[str, Any]:
        endpoint = self.endpoint_builder(f'/v1/chains/{self.chain_name}/accounts/{wallet_address}')
        return self._make_request(endpoint)


    def get_recent_wallet_activity(
            self,
            hours_back: int = 24,
            activity_type: Optional[str] = None
    ) -> Dict[str, Any]:
        to_time = datetime.datetime.utcnow()
        from_time = to_time - datetime.timedelta(hours=hours_back)
        return self.get_activity_history(from_time, to_time, activity_type=activity_type)

    def get_collections(self, page_size: int = 100, page_cursor: Optional[str] = None) -> Dict[str, Any]:
        endpoint = self.endpoint_builder(f'/v1/chains/{self.chain_name}/collections')
        params = {'page_size': min(page_size, 200)}
        if page_cursor:
            params['page_cursor'] = page_cursor
        return self._make_request(endpoint, params)

    def get_nft_by_collection_and_id(self, collection_address: str, nft_id: str) -> Dict[str, Any]:
        endpoint = self.endpoint_builder(f'/v1/chains/{self.chain_name}/collections/{collection_address}/nfts/{nft_id}')
        return self._make_request(endpoint)

if __name__ == '__main__':
    api = ImmutableAPI()

    # Test activity history (this works)
    print("Testing activity history...")
    activity = api.get_recent_wallet_activity(hours_back=24, activity_type='transfer')
    print(f"Recent transfers: {activity}\n")

    # Test wallet NFTs
    print("Testing wallet NFTs...")
    wallet = '0x9c0a517041caeaf3eae8817b489179222e545f31'
    nfts = api.get_wallet_nfts(wallet)
    print(f"Wallet NFTs: {nfts}\n")

    # Test wallet token balances
    print("Testing wallet account details...")
    account = api.get_wallet_token_balances(wallet)
    print(f"Account details: {account}\n")