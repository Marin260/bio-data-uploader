package api

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"

	"github.com/gin-gonic/gin"
)

// TODO: log activity
func FileUpload(c *gin.Context){
	log.Println("file-upload-controller::FileUpload() - Enter")
	// Get file from form
	fmt.Println(c.Request)
	log.Println("Reading the request")
	file, handler, err := c.Request.FormFile("file")
	if err != nil{
		customError := fmt.Sprintf("Error while getting the file from the submited form - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return 
	}
	defer file.Close()

	// Check if the file is to big
	if handler.Size > 3000000 {
		MalformedRequest(c, int(handler.Size))
		return 
	}

	// Create new local file
	log.Println("Creating a new file")
	dstFile, err := os.Create("./../output/" + handler.Filename)
	if err != nil {
		customError := fmt.Sprintf("Error while creating a local file - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return 
	}
	defer dstFile.Close()

	// Copy form file into new file
	log.Println("Copying request file content to the newly created file")
	_, err = io.Copy(dstFile, file)
	if err != nil {
		customError := fmt.Sprintf("Error while copying file content - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return 
	}

	fileName := strings.TrimSuffix(handler.Filename, ".txt")
	// Run python script
	log.Println("Running Python script")
	out, err := exec.Command("python3", "../py/sleep_analysis.py", "-fn", fileName).CombinedOutput()
	if err != nil {
		customError := fmt.Sprintf("Error while runinng the script - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return 
	}
	fmt.Println(string(out))

	c.Writer.Header().Set("Content-Type", "application/json")
	c.JSON(http.StatusOK, gin.H{
		"message": fileName,
	})

	// Remove all created files to free up space
	log.Println("Deleting files created by the python script")
	scriptOutDir := strings.Split(fileName, "Ct")[1]
	fmt.Println("This is the out folder Aloooo", scriptOutDir) 
	os.RemoveAll("./../output/" + scriptOutDir)
	os.RemoveAll("./../output/sleep")
	os.Remove("./../output/" + fileName + ".txt")

	log.Println("file-upload-controller::FileUpload() - Exit")
	return 
}