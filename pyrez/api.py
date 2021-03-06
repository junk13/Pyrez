from datetime import timedelta, datetime
from hashlib import md5 as getMD5Hash
from sys import version_info as pythonVersion
import requests

import pyrez
from pyrez.enumerations import *
from pyrez.exceptions import *
from pyrez.http import HttpRequest as HttpRequest
from pyrez.models import *

class BaseAPI:
    """
    DON'T INITALISE THIS YOURSELF!

    Parameters
    ----------
    devId : int
        Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
    authKey : str
        Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
    endpoint : class:`Endpoint`
        The endpoint that will be used by default for outgoing requests.
    responseFormat : [optional] : class:`ResponseFormat`
        The response format that will be used by default when making requests.
        Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
    """
    def __init__(self, devId, authKey, endpoint, responseFormat = ResponseFormat.JSON, header = None):
        """
        Parameters
        ----------
        devId : int
            Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
        authKey : str
            Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
        endpoint : class:`Endpoint`
            The endpoint that will be used by default for outgoing requests.
        responseFormat : [optional] : class:`ResponseFormat`
            The response format that will be used by default when making requests.
            Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
        """
        if not devId or not authKey:
            raise IdOrAuthEmptyException("DevId or AuthKey not specified!")
        elif len(str(devId)) != 4 or not str(devId).isnumeric():
            raise InvalidArgumentException("You need to pass a valid DevId!")
        elif len(str(authKey)) != 32 or not str(authKey).isalnum():
            raise InvalidArgumentException("You need to pass a valid AuthKey!")
        elif len(str(endpoint)) == 0 :
            raise InvalidArgumentException("Endpoint can't be empty!")
        self.__devId__ = int(devId)
        self.__authKey__ = str(authKey)
        self.__endpointBaseURL__ = str(endpoint)
        self.__responseFormat__ = ResponseFormat(responseFormat) if isinstance(responseFormat, ResponseFormat) else ResponseFormat.JSON
        self.__header__ = header
        
    def __encode__(self, string, encodeType = "utf-8"):
        return str(string).encode(encodeType)

    def __decode__(self, string, encodeType = "utf-8"):
        return str(string).encode(encodeType)

    def __httpRequest__(self, url, header = None):
        httpResponse = HttpRequest(header if header else self.__header__).get(url)
        if httpResponse.status_code >= 400:
            raise NotFoundException("Wrong URL: {0}".format(httpResponse.text))
        if httpResponse.status_code == 200:
            try:
                return httpResponse.json()
            except:
                return httpResponse.text

class HiRezAPI(BaseAPI):
    """
    Class for handling connections and requests to Hi-Rez Studios APIs. IS BETTER DON'T INITALISE THIS YOURSELF!

    Parameters
    ----------
    devId : int
        Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
    authKey : str
        Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
    endpoint : class:`Endpoint`
        The endpoint that will be used by default for outgoing requests.
    responseFormat : [optional] : class:`ResponseFormat`
        The response format that will be used by default when making requests.
        Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
    """

    PYREZ_HEADER = { "user-agent": "{0} [Python/{1.major}.{1.minor}]".format(pyrez.__title__, pythonVersion) }

    def __init__(self, devId, authKey, endpoint, responseFormat = ResponseFormat.JSON, sessionId = None):
        """
        Parameters
        ----------
        devId : int
            Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
        authKey : str
            Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
        endpoint : class:`Endpoint`
            The endpoint that will be used by default for outgoing requests.
        responseFormat : [optional] : class:`ResponseFormat`
            The response format that will be used by default when making requests.
            Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
        """
        super().__init__(devId, authKey, endpoint, responseFormat, self.PYREZ_HEADER)
        self.currentSessionId = sessionId if sessionId and str(sessionId).isalnum() else None

    def __createTimeStamp__(self, format = "%Y%m%d%H%M%S"):
        """
        Parameters
        ----------
        format : str
            Format of timeStamp

        Returns
        -------
            Returns the current time formatted
        """
        return self.__currentTime__().strftime(format)

    def __currentTime__(self):
        """
        
        Returns
        -------
            Returns the current UTC time
        """
        return datetime.utcnow()

    def __createSignature__(self, method, timestamp = None):
        """
        Parameters
        ----------
        method : str
            Method name
        timestamp : str
            Format of timeStamp
            
        Returns
        -------
            Returns a Signature hash of the method
        """
        return getMD5Hash(self.__encode__(str(self.__devId__) + str(method) + str(self.__authKey__) + str(timestamp if timestamp else self.__createTimeStamp__()))).hexdigest()

    def __sessionExpired__(self):
        return self.currentSessionId is None or not str(self.currentSessionId).isalnum()

    def __buildUrlRequest__(self, apiMethod, params =()): # [queue, date, hour]
        if len(str(apiMethod)) == 0:
            raise InvalidArgumentException("No API method specified!")
        #urlRequest = '/'.join(self.__endpointBaseURL__, apiMethod.lower(), self.__responseFormat__)
        urlRequest = "{0}/{1}{2}".format(self.__endpointBaseURL__, apiMethod.lower(), self.__responseFormat__)
        if apiMethod.lower() != "ping":
            urlRequest += "/{0}/{1}".format(self.__devId__, self.__createSignature__(apiMethod.lower()))
            if self.currentSessionId != None and apiMethod.lower() != "createsession":
                urlRequest += "/{0}".format(self.currentSessionId)
            urlRequest += "/{0}".format(self.__createTimeStamp__())
            #if self.currentSessionId != None and apiMethod.lower() != "createsession":
                #urlRequest = [ self.__endpointBaseURL__, apiMethod.lower(), self.__responseFormat__, self.dev_id, self.__createSignature__(apiMethod.lower()), self.currentSessionId, self.currentSession.sessionId, self.__createTimeStamp__() ]
            #else:
                #urlRequest = [ self.__endpointBaseURL__, apiMethod.lower(), self.__responseFormat__, self.dev_id, self.__createSignature__(apiMethod.lower()), self.currentSessionId, self.__createTimeStamp__() ]
            if params:
                #urlRequest += "/" + [str(param) for param in params]
                #stringParam += param.strftime("yyyyMMdd") if isinstance(param, datetime) else(param is Enums.QueueType || param is Enums.eLanguageCode) ?((int) param).ToString() : str(param);
                for param in params:
                    if param != None:
                        #.strftime("%Y%m%d") # urlRequest += '/' + param.strftime("yyyyMMdd") if isinstance(param, datetime) else str(param)
                        urlRequest += "/{0}".format(param.strftime("yyyyMMdd") if isinstance(param, datetime) else str(param.value) if isinstance(param, IntFlag) or isinstance(param, Enum) else str(param))
        return urlRequest.replace(' ', "%20")

    def makeRequest(self, apiMethod, params =()):
        if len(str(apiMethod)) == 0:
            raise InvalidArgumentException("No API method specified!")
        elif(apiMethod.lower() != "createsession" and self.__sessionExpired__()):
            self.__createSession__()
        result = self.__httpRequest__(apiMethod if str(apiMethod).lower().startswith("http") else self.__buildUrlRequest__(apiMethod, params))
        if result:
            if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
                return result
            else:
                if str(result).lower().find("ret_msg") == -1:
                    return None if len(str(result)) == 2 and str(result) == "[]" else result
                else:
                    hasError = APIResponse(**result) if str(result).startswith('{') else APIResponse(**result[0])
                    if hasError != None and hasError.hasRetMsg():
                        if hasError.retMsg == "Approved":
                            self.currentSessionId = Session(**result).sessionId
                        elif hasError.retMsg.find("dailylimit") != -1:
                            raise DailyLimitException("Daily limit reached: " + hasError.retMsg)
                        elif hasError.retMsg.find("Maximum number of active sessions reached") != -1:
                            raise SessionLimitException("Concurrent sessions limit reached: " + hasError.retMsg)
                        elif hasError.retMsg.find("Invalid session id") != -1:
                            self.__createSession__()
                            return self.makeRequest(apiMethod, params)
                        elif hasError.retMsg.find("Exception while validating developer access") != -1:
                            raise WrongCredentials("Wrong credentials: " + hasError.retMsg)
                        elif hasError.retMsg.find("404") != -1:
                            raise NotFoundException("Not found: " + hasError.retMsg)
                    return result

    def switchEndpoint(self, endpoint):
        if not isinstance(endpoint, Endpoint):
            raise InvalidArgumentException("You need to use the Endpoint enum to switch endpoints")
        self.__endpointBaseURL__ = str(endpoint)

    def __createSession__(self):
        """
        /createsession[ResponseFormat]/{devId}/{signature}/{timestamp}
        A required step to Authenticate the devId/signature for further API use.
        """
        try:
            tempResponseFormat = self.__responseFormat__
            self.__responseFormat__ = ResponseFormat.JSON
            responseJSON = self.makeRequest("createsession")
            self.__responseFormat__ = tempResponseFormat
            return Session(**responseJSON) if responseJSON else None
        except WrongCredentials as x:
            raise x
    
    def ping(self):
        """
        /ping[ResponseFormat]
        A quick way of validating access to the Hi-Rez API.
        
        Returns
        -------
        Object of :class:`Ping`
            Returns the infos about the API.
        """
        tempResponseFormat = self.__responseFormat__
        self.__responseFormat__ = ResponseFormat.JSON
        responseJSON = self.makeRequest("ping")
        self.__responseFormat__ = tempResponseFormat
        return Ping(responseJSON) if responseJSON else None
    
    def testSession(self, sessionId = None):
        """
        /testsession[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}
        A means of validating that a session is established.

        Parameters
        ----------
        sessionId : str
        
        Returns
        -------
        Object of :class:`TestSession`
        """
        session = self.currentSessionId if sessionId is None or not str(sessionId).isalnum() else sessionId
        uri = "{0}/testsession{1}/{2}/{3}/{4}/{5}".format(self.__endpointBaseURL__, self.__responseFormat__, self.__devId__, self.__createSignature__("testsession"), session, self.__createTimeStamp__())
        result = self.__httpRequest__(uri)
        return result.find("successful test") != -1

    def getDataUsed(self):
        """
        /getdataused[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}
        Returns API Developer daily usage limits and the current status against those limits.
        
        Returns
        -------
        Object of :class:`DataUsed`

        """
        tempResponseFormat = self.__responseFormat__
        self.__responseFormat__ = ResponseFormat.JSON
        responseJSON = self.makeRequest("getdataused")
        self.__responseFormat__ = tempResponseFormat
        return None if responseJSON is None else DataUsed(**responseJSON) if str(responseJSON).startswith('{') else DataUsed(**responseJSON[0])
    
    def getHiRezServerFeeds(self):
        """
        A quick way of validating access to the Hi-Rez API.
        """
        req = self.__httpRequest__("http://status.hirezstudios.com/history.atom", self.__header__)
        return req
    
    def getHiRezServerStatus(self):
        """
        /gethirezserverstatus[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}
        Function returns UP/DOWN status for the primary game/platform environments. Data is cached once a minute.
        
        Returns
        -------
        Object of :class:`HiRezServerStatus`

        """
        tempResponseFormat = self.__responseFormat__
        self.__responseFormat__ = ResponseFormat.JSON
        responseJSON = self.makeRequest("gethirezserverstatus")
        self.__responseFormat__ = tempResponseFormat
        return None if responseJSON is None else HiRezServerStatus(**responseJSON) if str(responseJSON).startswith('{') else HiRezServerStatus(**responseJSON[0])

    def getPatchInfo(self):
        """
        /getpatchinfo[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}
        Function returns information about current deployed patch. Currently, this information only includes patch version.
        
        Returns
        -------
        Object of :class:`PatchInfo`

        """
        tempResponseFormat = self.__responseFormat__
        self.__responseFormat__ = ResponseFormat.JSON
        responseJSON = self.makeRequest("getpatchinfo")
        self.__responseFormat__ = tempResponseFormat
        return PatchInfo(**responseJSON) if responseJSON else None
    
    def getFriends(self, playerId):
        """
        /getfriends[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{playerId}
        Returns the User names of each of the player’s friends of one player. [PC only]
        
        Returns
        -------
        list of :class:`Friend` objects
            
        """

        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        responseJSON = self.makeRequest("getfriends", [playerId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return responseJSON
        else:
            if not responseJSON:
                return None
            friends = []
            for friend in responseJSON:
                obj = Friend(**friend)
                friends.append(obj)
            return friends if friends else None

    def getMatchDetails(self, matchId):
        """
        /getmatchdetails[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{matchId}
        Returns the statistics for a particular completed match.
        
        Parameters
        ----------
        matchId : int
        """
        if not matchId or not str(matchId).isnumeric():
            raise InvalidArgumentException("Invalid Match ID!")
        return self.makeRequest("getmatchdetails", [matchId])
    
    def getMatchDetailsBatch(self, matchIds =()): #5-10 partidas
        """
        /getmatchdetailsbatch[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{matchId,matchId,matchId,...matchId}
        Returns the statistics for a particular set of completed matches.

        Parameters
        ----------
        matchIds : list

        NOTE
        ----------
        There is a byte limit to the amount of data returned;
        Please limit the CSV parameter to 5 to 10 matches because of this and for Hi-Rez DB Performance reasons.
        
        """
        return self.makeRequest("getmatchdetailsbatch", [matchIds])

    def getMatchHistory(self, playerId):
        """
        /getmatchhistory[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{playerId}
        Gets recent matches and high level match statistics for a particular player.

        Parameters
        ----------
        playerId : int
        """
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        getMatchHistoryResponse = self.makeRequest("getmatchhistory", [playerId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getMatchHistoryResponse
        else:
            if not getMatchHistoryResponse:
                return None
            matchHistorys = []
            for i in range(0, len(getMatchHistoryResponse)):
                obj = MatchHistory(**getMatchHistoryResponse[i])
                matchHistorys.append(obj)
            return matchHistorys if matchHistorys else None

    def getMatchIdsByQueue(self, queueId, date, hour = -1):
        """
        /getmatchidsbyqueue[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{queue}/{date}/{hour}
        Lists all Match IDs for a particular Match Queue; useful for API developers interested in constructing data by Queue.
        To limit the data returned, an {hour} parameter was added (valid values: 0 - 23).
        An {hour} parameter of -1 represents the entire day, but be warned that this may be more data than we can return for certain queues.
        Also, a returned “active_flag” means that there is no match information/stats for the corresponding match.
        Usually due to a match being in-progress, though there could be other reasons.

        Parameters
        ----------
        queueId : int
        date : int
        hour : int

        NOTE
        ----------
        To avoid HTTP timeouts in the GetMatchIdsByQueue() method, you can now specify a 10-minute window within the specified {hour} field to lessen the size of data returned by appending a “,mm” value to the end of {hour}.
        For example, to get the match Ids for the first 10 minutes of hour 3, you would specify {hour} as “3,00”.
        This would only return the Ids between the time 3:00 to 3:09.
        Rules below:
            Only valid values for mm are “00”, “10”, “20”, “30”, “40”, “50”
            To get the entire third hour worth of Match Ids, call GetMatchIdsByQueue() 6 times, specifying the following values for {hour}: “3,00”, “3,10”, “3,20”, “3,30”, “3,40”, “3,50”.
            The standard, full hour format of {hour} = “hh” is still supported.
        """
        return self.makeRequest("getmatchidsbyqueue", [queueId, date.strftime("%Y%m%d") if isinstance(date, datetime) else date, hour])
    #Need to test
    def getPlayer(self, playerId, portalId = None):
        """
        /getplayer[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{player}
        /getplayer[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{player}/{portalId}
        Returns league and other high level data for a particular player.

        Parameters
        ----------
        playerId : int or str
        """
        if not playerId or len(str(playerId)) <= 3:
            raise InvalidArgumentException("Invalid player!")
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return self.makeRequest("getplayer", [playerId, portalId]) if portalId else self.makeRequest("getplayer", [playerId])
        else:
            if isinstance(self, RealmRoyaleAPI):
                plat = "hirez" if not str(playerId).isdigit() or str(playerId).isdigit() and len(str(playerId)) <= 8 else "steam"
                return PlayerRealmRoyale(**self.makeRequest("getplayer", [playerId, plat]))
            else:
                res = self.makeRequest("getplayer", [playerId, portalId]) if portalId else self.makeRequest("getplayer", [playerId])
                if res:
                    return PlayerSmite(**res[0]) if isinstance(self, SmiteAPI) else PlayerPaladins(**res[0])
                else:
                    return None

    #Need to test
    def getPlayerAchievements(self, playerId):
        """
        /getplayerachievements[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{playerId}
        Returns select achievement totals (Double kills, Tower Kills, First Bloods, etc) for the specified playerId.

        Parameters
        ----------
        playerId : int
        """
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        getPlayerAchievementsResponse = self.makeRequest("getplayerachievements", [playerId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getPlayerAchievementsResponse
        else:
            if not getPlayerAchievementsResponse:
                return None
            return PlayerAcheviements(**getPlayerAchievementsResponse) if str(getPlayerAchievementsResponse).startswith('{') else PlayerAcheviements(**getPlayerAchievementsResponse[0])

    #Need to test
    def getPlayerIdByName(self, playerName):
        """
        /getplayeridbyname[ResponseFormat]/{developerId}/{signature}/{session}/{timestamp}/{playerName}
        Function returns a list of Hi-Rez playerId values (expected list size = 1) for playerName provided. The playerId returned is
        expected to be used in various other endpoints to represent the player/individual regardless of platform.

        Parameters
        ----------
        playerId : int or str
        """
        return self.makeRequest("getplayeridbyname", [playerName])
    #Need to test
    def getPlayerIdByPortalUserId(self, portalId, portalUserId):
        """
        /getplayeridbyportaluserid[ResponseFormat]/{developerId}/{signature}/{session}/{timestamp}/{portalId}/{portalUserId}
        Function returns a list of Hi-Rez playerId values (expected list size = 1) for {portalId}/{portalUserId} combination provided.
        The playerId returned is expected to be used in various other endpoints to represent the player/individual regardless of platform.

        Parameters
        ----------
        playerId : int or str
        """
        return self.makeRequest("getplayeridbyportaluserid", [portalId, portalUserId])
    #Need to test
    def getPlayerIdByPortalUserId(self, portalId, gamerTag):
        """
        /getplayeridsbygamertag[ResponseFormat]/{developerId}/{signature}/{session}/{timestamp}/{portalId}/{gamerTag}
        Function returns a list of Hi-Rez playerId values for {portalId}/{portalUserId} combination provided. The appropriate
        playerId extracted from this list by the API end user is expected to be used in various other endpoints to represent the player/individual regardless of platform.

        Parameters
        ----------
        playerId : int or str
        """
        return self.makeRequest("getplayeridsbygamertag", [portalId, gamerTag])
    def getPlayerStatus(self, playerId):
        """
        /getplayerstatus[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{playerId}
        Returns player status as follows:
            0 - Offline
            1 - In Lobby  (basically anywhere except god selection or in game)
            2 - god Selection (player has accepted match and is selecting god before start of game)
            3 - In Game (match has started)
            4 - Online (player is logged in, but may be blocking broadcast of player state)
            5 - Unknown (player not found)

        Parameters
        ----------
        playerId : int or str
        
        Returns
        -------
        Object of :class:`PlayerStatus`
            
        """
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        getPlayerStatusResponse = self.makeRequest("getplayerstatus", [playerId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getPlayerStatusResponse
        else:
            if not getPlayerStatusResponse:
                return None
            return PlayerStatus(**getPlayerStatusResponse) if str(getPlayerStatusResponse).startswith('{') else PlayerStatus(**getPlayerStatusResponse[0]) if getPlayerStatusResponse else None
    #Need to test
    def getQueueStats(self, playerId, queueId):
        """
        /getqueuestats[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{playerId}/{queue}
        Returns match summary statistics for a (player, queue) combination grouped by gods played.

        Parameters
        ----------
        playerId : int or str
        queueId : int
        """
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")

        getQueueStatsResponse = self.makeRequest("getqueuestats", [playerId, queueId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getQueueStatsResponse
        else:
            if not getQueueStatsResponse:
                return None
            QueueStats = []
            for i in getQueueStatsResponse:
                obj = QueueStats(**i)
                QueueStats.append(obj)
            return QueueStats if QueueStats else None

class BaseSmitePaladinsAPI(HiRezAPI):
    """
    Class for handling connections and requests to Hi-Rez Studios APIs. IS BETTER DON'T INITALISE THIS YOURSELF!

    Parameters
    ----------
    devId : int
        Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
    authKey : str
        Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
    endpoint : class:`Endpoint`
        The endpoint that will be used by default for outgoing requests.
    responseFormat : [optional] : class:`ResponseFormat`
        The response format that will be used by default when making requests.
        Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
    """
    def __init__(self, devId, authKey, endpoint, responseFormat = ResponseFormat.JSON, sessionId = None):
        """
        Parameters
        ----------
        devId : int
            Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
        authKey : str
            Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
        endpoint : class:`Endpoint`
            The endpoint that will be used by default for outgoing requests.
        responseFormat : [optional] : class:`ResponseFormat`
            The response format that will be used by default when making requests.
            Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
        """
        super().__init__(devId, authKey, endpoint, responseFormat, sessionId)
    def getGods(self, language = LanguageCode.English):
        """
        /getgods[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{languageCode}
        Returns all Gods and their various attributes.
        
        Parameters
        ----------
        language: [optional] : class: `LanguageCode` : 
        
        Returns
        -------
        Object of :class:`God` or :class:`Champion`
            Returns the infos about the API.

        """
        if not isinstance(self, PaladinsAPI) and not isinstance(self, SmiteAPI):
            raise NotSupported("This method is just for Paladins and Smite API's!")
        getGodsResponse = self.makeRequest("getgods", [language])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getGodsResponse
        else:
            if not getGodsResponse:
                return None
            gods = []
            for i in getGodsResponse:
                obj = God(**i) if isinstance(self, SmiteAPI) else Champion(**i)
                gods.append(obj)
            return gods if gods else None

    def getGodRanks(self, playerId):
        """
        /getgodranks[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{playerId}
        Returns the Rank and Worshippers value for each God a player has played.
        
        Parameters
        ----------
        playerId : int or str
        
        Returns
        -------
        Object of :class:`GodRank`

        """
        if not isinstance(self, PaladinsAPI) and not isinstance(self, SmiteAPI):
            raise NotSupported("This method is just for Paladins and Smite API's!")
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        getGodRanksResponse = self.makeRequest("getgodranks", [playerId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getGodRanksResponse
        else:
            if not getGodRanksResponse:
                return None
            godRanks = []
            for i in getGodRanksResponse:
                godRanks.append(GodRank(**i))
            return godRanks if godRanks else None
    #Need to test
    def getGodSkins(self, godId, language = LanguageCode.English):
        """
        /getgodskins[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{godId}/{languageCode}
        Returns all available skins for a particular God.
        
        Parameters
        ----------
        godId: int : 
        language: :class:`LanguageCode`
        """
        getGodSkinsResponse = self.makeRequest("getgodskins", [godId, language])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getGodSkinsResponse
        else:
            if not getGodSkinsResponse:
                return None
            godSkins = []
            for godSkin in getGodSkinsResponse:
                obj = GodSkin(**godSkin) if isinstance(self, SmiteAPI) != -1 else ChampionSkin(**godSkin)
                godSkins.append(obj)
            return godSkins if godSkins else None
    
    def getItems(self, language = LanguageCode.English):
        """
        /getitems[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{languageCode}
        Returns all Items and their various attributes.
        
        Parameters
        ----------
        language : [optional] :class:`LanguageCode`
        """
        return self.makeRequest("getitems", [language])
class PaladinsAPI(BaseSmitePaladinsAPI):
    """
    Class for handling connections and requests to Paladins API.

    Parameters
    ----------
    devId : int
        Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
    authKey : str
        Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
    endpoint : class:`Endpoint`
        The endpoint that will be used by default for outgoing requests.
    responseFormat : [optional] : class:`ResponseFormat`
        The response format that will be used by default when making requests.
        Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
    """
    def __init__(self, devId, authKey, platform = Platform.PC, responseFormat = ResponseFormat.JSON, sessionId = None):
        """
        Parameters
        ----------
        devId : int
            Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
        authKey : str
            Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
        endpoint : class:`Endpoint`
            The endpoint that will be used by default for outgoing requests.
        responseFormat : [optional] : class:`ResponseFormat`
            The response format that will be used by default when making requests.
            Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
        """
        if platform == Platform.MOBILE:
            raise NotSupported("Not released yet!")
        endpoint = Endpoint.PALADINS_XBOX if platform == Platform.XBOX or platform == Platform.NINTENDO_SWITCH else Endpoint.PALADINS_PS4 if platform == Platform.PS4 else Endpoint.PALADINS_PC
        super().__init__(devId, authKey, endpoint, responseFormat, sessionId)

    def switchPlatform(self, platform):
        if not isinstance(endpoint, Platform):
            raise InvalidArgumentException("You need to use the Platform enum to switch platforms")
        self.__endpointBaseURL__ = str(Endpoint.PALADINS_XBOX) if platform == Platform.XBOX or platform == Platform.NINTENDO_SWITCH else str(Endpoint.PALADINS_PS4) if platform == Platform.PS4 else str(Endpoint.PALADINS_PC)

    def getChampions(self, language = LanguageCode.English):
        """
        /getchampions[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{languageCode}
        Returns all Champions and their various attributes. [PaladinsAPI only]

        Parameters
        ----------
        language: [optional] : class:`LanguageCode`:  
        """
        getChampionsResponse = self.makeRequest("getchampions", [language]) # self.makeRequest("getgods", language)
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getChampionsResponse
        else:
            if not getChampionsResponse:
                return None
            champions = []
            for i in getChampionsResponse:
                obj = Champion(**i)
                champions.append(obj)
            return champions if champions else None
    #Needed to test
    def getChampionsCards(self, championId, language = LanguageCode.English):
        """
        /getchampioncards[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{championId}/{languageCode}
        Returns all Champion cards. [PaladinsAPI only]

        Parameters
        ----------
        language: [optional] : class:`LanguageCode`:  
        """
        getChampionsCardsResponse = self.makeRequest("getchampioncards", [championId, language])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getChampionsCardsResponse
        else:
            if not getChampionsCardsResponse:
                return None
            cards = []
            for i in getChampionsCardsResponse:
                obj = ChampionCard(**i)
                cards.append(obj)
            return cards if cards else None

    def getChampionLeaderboard(self, champId, queue = 428):
        """
        /getchampionleaderboard[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{godId}/{queue}
        Returns the current season’s leaderboard for a champion/queue combination. [PaladinsAPI; only queue 428]
        
        Parameters
        ----------
        champId : int
        """
        if not champId or len(str(champId)) != 4:
            raise InvalidArgumentException("Invalid Champion ID!")
        getChampionLeaderboardResponse = self.makeRequest("getchampionleaderboard", [champId, queue])
        return getChampionLeaderboardResponse
    def getChampionRanks(self, playerId):
        """
        /getchampionranks[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{playerId}
        Returns the Rank and Worshippers value for each Champion a player has played. [PaladinsAPI only]
        
        Parameters
        ----------
        playerId : int or str
        """
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        getChampionsRanksResponse = self.makeRequest("getgodranks", [playerId]) # self.makeRequest("getchampionranks", [playerId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getChampionsRanksResponse
        else:
            if not getChampionsRanksResponse:
                return None
            championRanks = []
            for i in getChampionsRanksResponse:
                championRanks.append(GodRank(**i))
            return championRanks if championRanks else None

    def getChampionRecommendedItems(self, champId, language = LanguageCode.English):
        """
        /getchampionrecommendeditems[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{godId}/{languageCode}
        Returns the Recommended Items for a particular Champion. [PaladinsAPI only]
        
        Parameters
        ----------
        champId : int 
        language : class:`LanguageCode`
        
        Warning
        ----------
        OSBSOLETE - NO DATA RETURNED
        """
        return self.makeRequest("getchampionrecommendeditems", [champId, language])
        #raise DeprecatedException("OSBSOLETE - NO DATA RETURNED")
    #Need to test
    def getChampionSkins(self, champId, language = LanguageCode.English):
        """
        /getchampionskins[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{godId}/{languageCode}
        Returns all available skins for a particular Champion. [PaladinsAPI only]
        
        Parameters
        ----------
        champID : int
        language :class:`LanguageCode`
        """
        getChampSkinsResponse = self.makeRequest("getchampionskins", [champId, language])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getChampSkinsResponse
        else:
            if not getChampSkinsResponse:
                return None
            champSkins = []
            for champSkin in getChampSkinsResponse:
                obj = ChampionSkin(**champSkin)
                champSkins.append(obj)
            return champSkins if champSkins else None

    def getMatchPlayerDetails(self, matchId):
        """
        /getmatchplayerdetails[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{matchId}
        Returns player information for a live match.

        Parameters
        ----------
        matchId : int
        """
        if not matchId or not str(matchId).isnumeric():
            raise InvalidArgumentException("Invalid Match ID!")
        responseJSON = self.makeRequest("getmatchplayerdetails", [matchId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return responseJSON
        else:
            if not responseJSON:
                return None
            players = []
            for player in responseJSON:
                obj = MatchPlayerDetail(**player)
                players.append(obj)
            return players if players else None

    def getPlayerIdInfoForXboxAndSwitch(self, playerName):
        """
        /getplayeridinfoforxboxandswitch[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{playerName}
        Meaningful only for the Paladins Xbox API. Paladins Xbox data and Paladins Switch data is stored in the same DB.
        Therefore a Paladins Gamer Tag value could be the same as a Paladins Switch Gamer Tag value.
        Additionally, there could be multiple identical Paladins Switch Gamer Tag values.
        The purpose of this method is to return all Player ID data associated with the playerName (gamer tag) parameter.
        The expectation is that the unique player_id returned could then be used in subsequent method calls. [PaladinsAPI only]
        """
        return self.makeRequest("getplayeridinfoforxboxandswitch", [playerName])

    def getPlayerLoadouts(self, playerId, language = LanguageCode.English):
        """
        /getplayerloadouts[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/playerId}/{languageCode}
        Returns deck loadouts per Champion. [PaladinsAPI only]
        
        Parameters
        ----------
        playerId : int or str
        language: :class:`LanguageCode`
        """
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        getPlayerLoadoutsResponse = self.makeRequest("getplayerloadouts", [playerId, language])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getPlayerLoadoutsResponse
        else:
            if not getPlayerLoadoutsResponse:
                return None
            playerLoadouts = []
            for i in range(0, len(getPlayerLoadoutsResponse)):
                obj = PlayerLoadout(**getPlayerLoadoutsResponse[i])
                playerLoadouts.append(obj)
            return playerLoadouts if playerLoadouts else None
        
class RealmRoyaleAPI(HiRezAPI):
    """
    Class for handling connections and requests to Realm Royale API.

    Parameters
    ----------
    devId : int
        Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
    authKey : str
        Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
    endpoint : class:`Endpoint`
        The endpoint that will be used by default for outgoing requests.
    responseFormat : [optional] : class:`ResponseFormat`
        The response format that will be used by default when making requests.
        Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
    """
    def __init__(self, devId, authKey, platform = Platform.PC, responseFormat = ResponseFormat.JSON, sessionId = None):
        """
        Parameters
        ----------
        devId : int
            Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
        authKey : str
            Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
        endpoint : class:`Endpoint`
            The endpoint that will be used by default for outgoing requests.
        responseFormat : [optional] : class:`ResponseFormat`
            The response format that will be used by default when making requests.
            Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
        """
        if platform != Platform.PC:
            raise NotSupported("Not released yet!")
        endpoint = Endpoint.REALM_ROYALE_XBOX if(platform == Platform.XBOX) else Endpoint.REALM_ROYALE_PS4 if(platform == Platform.PS4) else Endpoint.REALM_ROYALE_PC
        super().__init__(devId, authKey, endpoint, responseFormat, sessionId)

    # /getplayermatchhistory[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{player}
    def getPlayerMatchHistory(self, playerId):
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        return self.makeRequest("getplayermatchhistory", [playerId])
    
    # /getplayermatchhistoryafterdatetime[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{player}/{startDatetime}
    def getPlayerMatchHistoryAfterDatetime(self, playerId, startDatetime):
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        return self.makeRequest("getplayermatchhistoryafterdatetime", [playerId, startDatetime])

    # /getplayerstats[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{player}
    def getPlayerStats(self, playerId):
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        return self.makeRequest("getplayerstats", [playerId])

    # /searchplayers[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{player}
    def searchPlayers(self, playerId):
        if not playerId or not str(playerId).isnumeric():
            raise InvalidArgumentException("Invalid player!")
        searchPlayerResponse = self.makeRequest("searchplayers", [playerId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return searchPlayerResponse
        else:
            if not searchPlayerResponse:
                return None
            players = []
            for player in searchPlayerResponse:
                obj = Player(**player)
                players.append(obj)
            return players if players else None

class SmiteAPI(BaseSmitePaladinsAPI):
    """
    Class for handling connections and requests to Smite API.

    Parameters
    ----------
    devId : int
        Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
    authKey : str
        Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
    endpoint : class:`Endpoint`
        The endpoint that will be used by default for outgoing requests.
    responseFormat : [optional] : class:`ResponseFormat`
        The response format that will be used by default when making requests.
        Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
    """
    def __init__(self, devId, authKey, platform = Platform.PC, responseFormat = ResponseFormat.JSON, sessionId = None):
        """
        Parameters
        ----------
        devId : int
            Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
        authKey : str
            Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
        endpoint : class:`Endpoint`
            The endpoint that will be used by default for outgoing requests.
        responseFormat : [optional] : class:`ResponseFormat`
            The response format that will be used by default when making requests.
            Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
        """
        if platform == Platform.NINTENDO_SWITCH or platform == Platform.MOBILE:
            raise NotSupported("Not released yet!")
        endpoint = Endpoint.SMITE_XBOX if(platform == Platform.XBOX) else Endpoint.SMITE_PS4 if(platform == Platform.PS4) else Endpoint.SMITE_PC
        super().__init__(devId, authKey, endpoint, responseFormat, sessionId)

    def switchPlatform(self, platform):
        if not isinstance(endpoint, Platform):
            raise InvalidArgumentException("You need to use the Platform enum to switch platforms")
        self.__endpointBaseURL__ = str(Endpoint.SMITE_XBOX) if platform == Platform.XBOX else str(Endpoint.SMITE_PS4) if platform == Platform.PS4 else str(Endpoint.SMITE_PC)

    def getDemoDetails(self, matchId):
        """
        /getdemodetails[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{matchId}
        Returns information regarding a particular match.  Rarely used in lieu of getmatchdetails().
        
        Parameters
        ----------
        matchId : int 
        
        """
        if not matchId or not str(matchId).isnumeric():
            raise InvalidArgumentException("Invalid Match ID!")
        return self.makeRequest("getdemodetails", [matchId])
    #Need to test
    def getEsportsProLeagueDetails(self):
        """
        /getesportsproleaguedetails[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}
        Returns the matchup information for each matchup for the current eSports Pro League season.
        An important return value is “match_status” which represents a match being scheduled (1), in-progress (2), or complete (3)
        """
        getEsportsProLeagueDetailsResponse = self.makeRequest("getesportsproleaguedetails")
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getEsportsProLeagueDetailsResponse
        else:
            if not getEsportsProLeagueDetailsResponse:
                return None
            details = []
            for detail in getEsportsProLeagueDetailsResponse:
                obj = EsportProLeagueDetail(**detail)
                details.append(obj)
            return details if details else None
    #Need to test
    def getGodLeaderboard(self, godId, queueId):
        """
        /getgodleaderboard[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{godId}/{queue}
        Returns the current season’s leaderboard for a god/queue combination. [SmiteAPI only; queues 440, 450, 451 only]
        
        Parameters
        ----------
        godId: int 
        queueId: int
        """
        getGodLeaderboardResponse = self.makeRequest("getgodleaderboard", [godId, queueId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getGodLeaderboardResponse
        else:
            if not getGodLeaderboardResponse:
                return None
            godLeaderb = []
            for leader in getGodLeaderboardResponse:
                obj = GodLeaderboard(**leader)
                godLeaderb.append(obj)
            return godLeaderb if godLeaderb else None
    
    def getGodRecommendedItems(self, godId, language = LanguageCode.English):
        """
        /getgodrecommendeditems[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{godId}/{languageCode}
        Returns the Recommended Items for a particular God. [SmiteAPI only]
        
        Parameters
        ----------
        godId : int
        language : [optional] : class: `LanguageCode` : 
        """
        return self.makeRequest("getgodrecommendeditems", [godId, language])
    
    def getLeagueLeaderboard(self, queueId, tier, season):
        """
        /getleagueleaderboard[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{queue}/{tier}/{season}
        Returns the top players for a particular league (as indicated by the queue/tier/season parameters).

        Parameters
        ----------
        queueId : int
        tier : int
        season : int
        """
        return self.makeRequest("getleagueleaderboard", [queueId, tier, season])

    def getLeagueSeasons(self, queueId):
        """
        /getleagueseasons[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{queue}
        Provides a list of seasons (including the single active season) for a match queue.

        Parameters
        ----------
        queueId : int
        """
        return self.makeRequest("getleagueseasons", [queueId])
    #Need to test
    def getMotd(self):
        """
        /getmotd[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}
        Returns information about the 20 most recent Match-of-the-Days.
        """
        getMOTDResponse = self.makeRequest("getmotd")
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getMOTDResponse
        else:
            if not getMOTDResponse:
                return None
            motds = []
            for motd in getMOTDResponse:
                obj = MOTD(**motd)
                motds.append(obj)
            return motds if motds else None
    #Need to test
    def getTeamDetails(self, clanId):
        """
        /getteamdetails[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{clanId}
        Lists the number of players and other high level details for a particular clan.
        
        Parameters
        ----------
        clanId: int
        """
        if not clanId or not str(clanId).isnumeric():
            raise InvalidArgumentException("Invalid Clan ID!")
        getTeamDetailsResponse = self.makeRequest("getteamdetails", [clanId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getTeamDetailsResponse
        else:
            if not getTeamDetailsResponse:
                return None
            teamDetails = []
            for teamDetail in getTeamDetailsResponse:
                obj = TeamDetail(**teamDetail)
                teamDetails.append(obj)
            return teamDetails if teamDetails else None
    
    def getTeamMatchHistory(self, clanId):
        """
        *DEPRECATED*

        /getteammatchhistory[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{clanId}
        Gets recent matches and high level match statistics for a particular clan/team.
        """
        if not clanId or not str(clanId).isnumeric():
            raise InvalidArgumentException("Invalid Clan ID!")
        raise DeprecatedException("*DEPRECATED* - As of 2.14 Patch, /getteammatchhistory is no longer supported and will return a NULL dataset.")
        #return self.makeRequest("getteammatchhistory", [clanId])
    #Need to test
    def getTeamPlayers(self, clanId):
        """
        /getteamplayers[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{clanId}
        Lists the players for a particular clan.
        
        Parameters
        ----------
        clanId: int
        """
        if not clanId or not str(clanId).isnumeric():
            raise InvalidArgumentException("Invalid Clan ID!")
        getTeamPlayers = self.makeRequest("getteamplayers", [clanId])
        if str(self.__responseFormat__).lower() == str(ResponseFormat.XML).lower():
            return getTeamPlayers
        else:
            if not getTeamPlayers:
                return None
            teamPlayers = []
            for teamPlayer in getTeamPlayers:
                obj = TeamPlayer(**teamPlayer)
                teamPlayers.append(obj)
            return teamPlayers if teamPlayers else None

    def getTopMatches(self):
        """
        /gettopmatches[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}
        Lists the 50 most watched / most recent recorded matches.
        """
        return self.makeRequest("gettopmatches")

    def searchTeams(self, teamId):
        """
        /searchteams[ResponseFormat]/{devId}/{signature}/{session}/{timestamp}/{searchTeam}
        Returns high level information for Clan names containing the “searchTeam” string. [SmiteAPI only]
        
        Parameters
        ----------
        teamId: int
        """
        return self.makeRequest("searchteams", [teamID])

class HandOfTheGodsAPI(HiRezAPI):
    """
    Class for handling connections and requests to Hand of the Gods API.

    Parameters
    ----------
    devId : int
        Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
    authKey : str
        Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
    endpoint : class:`Endpoint`
        The endpoint that will be used by default for outgoing requests.
    responseFormat : [optional] : class:`ResponseFormat`
        The response format that will be used by default when making requests.
        Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
    """
    def __init__(self, devId, authKey, responseFormat = ResponseFormat.JSON, sessionId = None):
        """
        Parameters
        ----------
        devId : int
            Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
        authKey : str
            Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
        endpoint : class:`Endpoint`
            The endpoint that will be used by default for outgoing requests.
        responseFormat : [optional] : class:`ResponseFormat`
            The response format that will be used by default when making requests.
            Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
        """
        raise NotSupported("Not released yet!")
        super().__init__(devId, authKey, Endpoint.HAND_OF_THE_GODS_PC, responseFormat, sessionId)

class PaladinsStrikeAPI(HiRezAPI):
    """
    Class for handling connections and requests to Paladins Strike API.

    Parameters
    ----------
    devId : int
        Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
    authKey : str
        Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
    endpoint : class:`Endpoint`
        The endpoint that will be used by default for outgoing requests.
    responseFormat : [optional] : class:`ResponseFormat`
        The response format that will be used by default when making requests.
        Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
    """
    def __init__(self, devId, authKey, responseFormat = ResponseFormat.JSON, sessionId = None):
        """
        Parameters
        ----------
        devId : int
            Used for authentication. This is the developer ID that you receive from Hi-Rez Studios.
        authKey : str
            Used for authentication. This is the authentication key that you receive from Hi-Rez Studios.
        endpoint : class:`Endpoint`
            The endpoint that will be used by default for outgoing requests.
        responseFormat : [optional] : class:`ResponseFormat`
            The response format that will be used by default when making requests.
            Otherwise, this will be used. It defaults to class:`ResponseFormat.JSON`.
        """
        raise NotSupported("Not released yet!")
        super().__init__(devId, authKey, Endpoint.PALADINS_STRIKE_MOBILE, responseFormat, sessionId)
