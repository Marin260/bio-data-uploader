package api

import (
	"fmt"
	"log"
	"os"

	"github.com/gin-gonic/gin"
)


func Sleep(c *gin.Context) {
	log.Println("img-controller::Sleep() - Enter")

	filePath := fmt.Sprintf("./../output/%s-sleep.png", c.Params.ByName("name"))
	// NOTE: this is a tmp comment, have to adjust to send zip insted of img
	//c.File(filePath)
	c.File("./../output/default.png")
	
	log.Println("Removing created png")
	err := os.Remove(filePath)
	if err != nil {
		fmt.Println("Error deleting sleep img", err)
	}

	log.Println("img-controller::Sleep() - Exit")
}

func Activity(c *gin.Context) {
	log.Println("img-controller::Activity() - Enter")

	filePath := fmt.Sprintf("./../output/%s-activity.png", c.Params.ByName("name"))
	//c.File(filePath)
	c.File("./../output/default.png")

	log.Println("Removing created png")
	err := os.Remove(filePath)
	if err != nil {
		fmt.Println("Error deleting activity img", err)
	}

	log.Println("img-controller::Activity() - Exit")
}