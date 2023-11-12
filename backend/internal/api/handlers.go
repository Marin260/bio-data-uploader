package api

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type BackendError struct {
	err string
	message string
	code int
}

func ErrorHandler(c *gin.Context, err BackendError){
	fmt.Println(err.err)

	log.Println("handlers::ErrorHandler() - Enter")
	log.Println("Error - " + err.err)
	c.JSON(err.code, gin.H{
		"status": err.code,
		"error": err.message,
	})
	log.Println("handlers::ErrorHandler() - Exit")
}

func MalformedRequest(c *gin.Context, size int){
	fmt.Println("File size to big")

	log.Println("handlers::MalformedRequest() - Enter")
	log.Printf("Error - file size to big | size - %d\n", size)
	c.JSON(http.StatusBadRequest, gin.H{
		"status": http.StatusBadRequest,
		"message": "File size to big",
	})
	log.Println("handlers::MalformedRequest() - Exit")
}

func Logger(param gin.LogFormatterParams) string {
	// your custom format
	return fmt.Sprintf("%s - [%s] \"%s %s %s %d %s \"%s\" %s\"\n",
			param.ClientIP,
			param.TimeStamp.Format(time.RFC1123),
			param.Method,
			param.Path,
			param.Request.Proto,
			param.StatusCode,
			param.Latency,
			param.Request.UserAgent(),
			param.ErrorMessage,
	)
}
