package api

import (
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

func HealthCheck(c *gin.Context){
	log.Println("health-check-controller::HealthCheck() - Enter")

	c.JSON(http.StatusOK, gin.H{
		"message": "pong",
	})
	
	log.Println("health-check-controller::HealthCheck() - Exit")
}