package api

import (
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
)

func Zip(c *gin.Context) {
	log.Println("file-controller::Zip() - Enter")

	// Sending file
	filePath := fmt.Sprintf("./output/%s.zip", c.Params.ByName("name"))
	c.File(filePath)

	// Delete zip
	log.Println("file-controller::Zip() - Removing created zip")
	err := os.Remove(filePath)
	err = os.RemoveAll(strings.TrimSuffix(filePath, ".zip"))
	if err != nil {
		log.Println("file-controller::Zip() - Error deleting zip", err)
	}

	log.Println("file-controller::Zip() - Exit")
}
