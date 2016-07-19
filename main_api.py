# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is a sample Hello World API implemented using Google Cloud
Endpoints."""

# [START imports]
import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote
# [END imports]

# [START import for DS]
from google.appengine.ext import ndb
# [END import for DS]


# [START entity declaration]
class LocationEntity(ndb.Model):
    lat = ndb.FloatProperty()
    long = ndb.FloatProperty()
# [STOP entity declaration]


# [START messages]
class Location(messages.Message):
    lat = messages.FloatField(1, required=True)
    long = messages.FloatField(2, required=True)
# [END messages]


# [START location_api]
@endpoints.api(name='location', version='v1')
class LocationApi(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(
        # The request body should be empty.
        message_types.VoidMessage,
        latitude=messages.FloatField(1, variant=messages.Variant.FLOAT),
        longitude=messages.FloatField(2, variant=messages.Variant.FLOAT)
    )

    @endpoints.method(
        # This method does not take a request message.
        GET_RESOURCE,
        # This method set location to database.
        Location,
        path='location/set',
        http_method='GET',
        name='location.set')
    def set_location(self, request):
        location = LocationEntity(lat=request.latitude, long=request.longitude, id='last_location')
        location.put()
        return Location(lat=location.lat, long=location.long)

    @endpoints.method(
        # This method does not take a request message.
        message_types.VoidMessage,
        # This method returns last location.
        Location,
        # The path defines the source of the URL parameter 'id'. If not
        # specified here, it would need to be in the query string.
        path='location/get',
        http_method='GET',
        name='location.get')
    def get_last_location(self, unused_request):
        key = ndb.Key(LocationEntity, 'last_location')
        location = key.get()
        return Location(lat=location.lat, long=location.long)
# [END location_api]


# [START auth_config]
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID
ALLOWED_CLIENT_IDS = [
    WEB_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID,
    endpoints.API_EXPLORER_CLIENT_ID]
# [END auth_config]

# [START api_server]
api = endpoints.api_server([LocationApi])
# [END api_server]
