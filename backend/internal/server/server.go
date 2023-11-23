package server

import (
	"io"
	"log"
	"os"

	"example.com/packages/internal/api"
	"github.com/gin-gonic/gin"
)

// TODO: add basic auth/basic JWT?
func BioServer() *gin.Engine{
	r := gin.Default()

	// Create a log file
	logfile, _ := os.Create("./logs/bio-request-logger.log")
	
	gin.DefaultWriter = io.MultiWriter(logfile)
	log.SetOutput(io.MultiWriter(logfile, gin.DefaultWriter))

	r.Use(CustomHeaders())
	r.Use(gin.LoggerWithFormatter(api.Logger))

	r.GET("/ping", api.HealthCheck)
	r.POST("/file-upload", api.FileUpload)
	r.GET("/zip/:name", api.Zip)

	return r
}

func CustomHeaders() gin.HandlerFunc {
	return func(c *gin.Context){
		c.Writer.Header().Set("Access-Control-Allow-Origin", "https://bio-dash.netlify.app/")
	}
}