package push

import (
	//"fmt"
	"net/http"
	"net/url"
	"strconv"
	"time"
	"sync"
	"fmt"
	//"runtime"
	"runtime"
)

var wg sync.WaitGroup
var requestIntervalFor200 = time.Millisecond * 100
var requestIntervalFor503 = time.Second * 180
var startSdkInterval = time.Millisecond *1
var acceptInterval = time.Millisecond *1100
var secondInterval = time.Millisecond *1000.
var pushIP = "192.168.4.181"
var pushPort = "9529"
var fileID = "561B90A24D754AC6FAFF7D3A54E9DA2A"
var requestPath = "http://"+pushIP+":"+pushPort+"/push/files/"+fileID+"/chunks/"
var cppc = "1"
var chunkGross = int(1000*1024*1024/304/1392) + 1
var chunkPerQuery = 12

func stress(sdk int) {
	defer wg.Done()

	var lastQueryChunks = 0
	var urlString string
	var startChunkId int

	send := time.Now()  // mark duration for one request
	last := time.Now()  // mark duration for request in one second

	for startChunkId = 0; startChunkId < chunkGross; {
		send = time.Now()

		// create url for HTTP request
		if startChunkId+ chunkPerQuery > chunkGross {
			lastQueryChunks = chunkGross % chunkPerQuery
			urlString = requestPath + strconv.Itoa(chunkGross-lastQueryChunks) + "_" + strconv.Itoa(lastQueryChunks) + "/pieces/" + cppc
		} else {
			urlString = requestPath + strconv.Itoa(startChunkId) + "_" + strconv.Itoa(chunkPerQuery) + "/pieces/" + cppc
		}

		// send out HTTP request
		u, _ := url.Parse(urlString)
		res, _ := http.Get(u.String())
		if startChunkId == 0 {
			defer res.Body.Close()
		}
		resCode := res.StatusCode
		res.Body.Close()

		// check response code
		duration := time.Since(send)
		if resCode == 200 {
			startChunkId += chunkPerQuery
			if requestIntervalFor200 > duration {
				durationSleep := requestIntervalFor200 - duration
				time.Sleep(durationSleep)
				if sdk > 100 && sdk % 50==0 && startChunkId % 120 == 0 {
					interval := time.Since(last)
					if interval < secondInterval {
						time.Sleep(secondInterval - interval)
					}
					interval = time.Since(last)
					result := "OK"
					if interval > acceptInterval {
						result = "BAD !!!!!!!!"
					}
					fmt.Printf("SDK-%d: 120 chucks cost: %f second - %d %s \n", sdk, interval.Seconds(), startChunkId, result)
					// Mark time
					last = time.Now()
				}
			}
		} else if resCode == 503 {
			fmt.Println("Get 503 ------------------------------------------------")
			time.Sleep(requestIntervalFor503)
		} else {
			fmt.Println("Get bad status code ************************************ ")
			break
		}

	}
}

func main() {
	runtime.GOMAXPROCS(32)
	sdkNum := 400
	wg.Add(sdkNum)

	for i:=0; i<sdkNum; i++ {
		go stress(i)
		time.Sleep(startSdkInterval)
	}
	fmt.Println("Start sdk done\n")
	wg.Wait()

}