package api

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"

	"github.com/gin-gonic/gin"
)

type ScriptInput struct {
	FilePath  string `json:"file_path"`
	FileName  string `json:"file_name"`
	StartDate string `json:"start_date"`
	EndDate   string `json:"end_date"`
}

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
	fileName := strings.TrimSuffix(handler.Filename, ".txt")
	dstFile, err := os.Create("./../output/" + fileName + ".csv")
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
	
	// Run python script
	startDate := c.Request.FormValue("start")
	endDate := c.Request.FormValue("end")
	scriptInputJSON := ScriptInput{FilePath: "./../output/" + fileName + ".csv", FileName: fileName, StartDate: startDate, EndDate: endDate }
	scriptInputFile, err := os.Create("./../output/" + fileName + ".json")
	if err != nil {
		customError := fmt.Sprintf("Error while creating a local file - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return 
	}
	defer scriptInputFile.Close()

	encoder := json.NewEncoder(scriptInputFile)
	err = encoder.Encode(scriptInputJSON)
	if err != nil {
		customError := fmt.Sprintf("Error while encoding json - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return
	}


	log.Println("Running Python script")
	out, err := exec.Command("python", "../py/sleep_analysis.py", "-fn", fileName+".json").CombinedOutput()
	if err != nil {
		fmt.Println("ALJO ", string(out))
		fmt.Println("ALJO ", err)
		customError := fmt.Sprintf("Error while runinng the script - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return 
	}
	fmt.Println(string(out))

	c.Writer.Header().Set("Content-Type", "application/json")
	c.JSON(http.StatusOK, gin.H{
		"fileName": fileName,
	})

	// TODO: clean up the error handling
	// TODO: clean up the logs
	// TODO: remove createt files by the script

	log.Println("file-upload-controller::FileUpload() - Exit")
	return 
}