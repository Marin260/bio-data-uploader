package server

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"example.com/packages/internal/api"
	"github.com/gin-gonic/gin"
)

// TODO: add basic auth/basic JWT?
func BioServer() *gin.Engine {
	r := gin.New()

	// Create a log file
	logfile, _ := os.Create("./logs/bio-request-logger.log")

	gin.DefaultWriter = io.MultiWriter(logfile)
	log.SetOutput(io.MultiWriter(logfile, gin.DefaultWriter))

	r.Use(CustomHeaders())
	r.Use(gin.LoggerWithFormatter(api.Logger))

	r.GET("/health/ping", api.HealthCheck)
	r.POST("/file/upload", api.FileUpload)
	r.GET("/zip/:name", api.Zip)

	return r
}

func CustomHeaders() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
	}
}

type Server struct {
	port int
}

func NewServer() *http.Server {
	port, _ := 5005, 0 //strconv.Atoi(os.Getenv("PORT"))
	NewServer := &Server{
		port: port,
	}

	// Declare Server config
	server := &http.Server{
		Addr:         fmt.Sprintf(":%d", NewServer.port),
		Handler:      NewServer.RegisterRoutes(),
		IdleTimeout:  time.Minute,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 30 * time.Second,
	}

	return server
}
