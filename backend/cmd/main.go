package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

// TODO: Logging
func main() {
	r := gin.Default()

	r.Use(CustomHeaders())

	r.GET("/ping", func(c *gin.Context){
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	r.POST("/csv-upload", func(c *gin.Context){
		// Get file from form
		fmt.Println(c.Request)
		time.Sleep(5)
		file, handler, err := c.Request.FormFile("file")
		if err != nil{
			fmt.Println("Error while getting the file from the submited form", err)
			errorHandler(c)
		}
		defer file.Close()

		// Check if the file is to big
		if handler.Size > 3000000 {
			malformedRequest(c)
		}
		fmt.Println("file name: ", handler.Filename)

		// Create new local file
		dstFile, err := os.Create("./../output/" + handler.Filename)
		if err != nil {
			fmt.Println("Error while creating a local file", err)
			errorHandler(c)
		}
		defer dstFile.Close()

		// Copy form file into new file
		_, err = io.Copy(dstFile, file)
		if err != nil {
			fmt.Print("Error while copying file content", err)
			errorHandler(c)
		}

		fileName := strings.TrimSuffix(handler.Filename, ".txt")
		// Run python script
		out, err := exec.Command("python3", "../py/sleep_analysis.py", "-fn", fileName).CombinedOutput()
		if err != nil {
			fmt.Println("Error while runinng the script", err)
			errorHandler(c)
		}
		fmt.Println(err)
		fmt.Println(string(out))

		c.Writer.Header().Set("Content-Type", "application/json")
		c.JSON(http.StatusOK, gin.H{
			"message": fileName,
		})

		// Remove all created files to free up space
		scriptOutDir := strings.Split(fileName, "Ct")[1]
		fmt.Println("This is the out folder Aloooo", scriptOutDir) 
		os.RemoveAll("./../output/" + scriptOutDir)
		os.RemoveAll("./../output/sleep")
		os.Remove("./../output/" + fileName + ".txt")
	})
	r.GET("/img/sleep/:name", func(c *gin.Context) {
		filePath := fmt.Sprintf("./../output/%s-sleep.png", c.Params.ByName("name"))
		c.File(filePath)
		err := os.Remove(filePath)
		if err != nil {
			fmt.Println("Error deleting sleep img", err)
		}
	})
	r.GET("/img/activity/:name", func(c *gin.Context) {
		filePath := fmt.Sprintf("./../output/%s-activity.png", c.Params.ByName("name"))
		c.File(filePath)
		err := os.Remove(filePath)
		if err != nil {
			fmt.Println("Error deleting activity img", err)
		}
	})

	r.Run(":8080")
}

func errorHandler(c *gin.Context){
	c.JSON(http.StatusInternalServerError, gin.H{
		"status": http.StatusInternalServerError,
		"error": "Internal server error",
	})
}

func malformedRequest(c *gin.Context){
	c.JSON(http.StatusBadRequest, gin.H{
		"status": http.StatusBadRequest,
		"message": "File size to big",
	})
}

func CustomHeaders() gin.HandlerFunc {
	return func(c *gin.Context){
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
	}
}