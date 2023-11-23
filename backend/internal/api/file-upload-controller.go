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

const outputPath = "./output/"

func FileUpload(c *gin.Context){
	log.Println("file-upload-controller::FileUpload() - Enter")

	// Get file from form
	log.Println("file-upload-controller::FileUpload() - Reading the request")
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
	log.Println("file-upload-controller::FileUpload() - Creating a new file")
	fileName := strings.TrimSuffix(handler.Filename, ".txt")
	dstFile, err := os.Create(outputPath + fileName + ".csv")
	if err != nil {
		customError := fmt.Sprintf("Error while creating a local file - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return 
	}

	// Copy form file into new file
	log.Println("file-upload-controller::FileUpload() - Copying request file content to the newly created file")
	_, err = io.Copy(dstFile, file)
	if err != nil {
		customError := fmt.Sprintf("Error while copying file content - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return 
	}
	
	// Prepare json input for the py script
	log.Println("file-upload-controller::FileUpload() - Creating json input")
	startDate := c.Request.FormValue("start")
	endDate := c.Request.FormValue("end")
	scriptInputJSON := ScriptInput{FilePath: outputPath + fileName + ".csv", FileName: fileName, StartDate: startDate, EndDate: endDate }
	scriptInputFile, err := os.Create(outputPath + fileName + ".json")
	if err != nil {
		customError := fmt.Sprintf("Error while creating a local file - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return 
	}
	
	encoder := json.NewEncoder(scriptInputFile)
	err = encoder.Encode(scriptInputJSON)
	if err != nil {
		customError := fmt.Sprintf("Error while encoding json - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return
	}
	
	// Run python script
	log.Println("file-upload-controller::FileUpload() - Running Python script")
	out, err := exec.Command("python3", "./py/sleep_analysis.py", "-fn", fileName+".json").CombinedOutput()
	if err != nil {
		fmt.Println(string(out))
		fmt.Println(err)
		customError := fmt.Sprintf("Error while runinng the script - %s", err)
		ErrorHandler(c, BackendError{err: customError, message: "Internal Server Error", code: http.StatusInternalServerError})
		return 
	}
	c.Writer.Header().Set("Content-Type", "application/json")
	c.JSON(http.StatusOK, gin.H{
		"fileName": fileName,
	})

	// Removing all the created files
	defer removeFiles(fileName, scriptInputFile, dstFile)
	fmt.Println(fileName)
	// TODO: clean up the error handling
	// TODO: remove createt files by the script

	log.Println("file-upload-controller::FileUpload() - Exit")
	return 
}

func removeFiles(fileName string, jsonFile *os.File, csvFile *os.File) {
	log.Println("file-upload-controller::removeFiles() - Enter")

	jsonFile.Close()
	csvFile.Close()

	log.Println("file-upload-controller::removeFiles() - Removing files")
	err := os.Remove(outputPath + fileName + ".json")
	if err != nil {
		log.Println("file-upload-controller::removeFiles() - Error while removing files:", err)
	}
	err = os.Remove(outputPath + fileName + ".csv")
	if err != nil {
		log.Println("file-upload-controller::removeFiles() - Error while removing files:", err)
	}

	log.Println("file-upload-controller::removeFiles() - Exit")
}