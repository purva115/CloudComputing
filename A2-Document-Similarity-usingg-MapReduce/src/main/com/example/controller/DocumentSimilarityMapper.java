package com.example.controller;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.StringTokenizer;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class DocumentSimilarityMapper extends Mapper<LongWritable, Text, Text, Text> {
    
    private Text documentId = new Text();
    private Text wordSet = new Text();
    
    @Override
    public void map(LongWritable key, Text value, Context context) 
            throws IOException, InterruptedException {
        
        String line = value.toString().trim();
        if (line.isEmpty()) {
            return;
        }
        
        // Split line into document ID and content
        String[] parts = line.split(" ", 2);
        if (parts.length < 2) {
            return;
        }
        
        String docId = parts[0];
        String content = parts[1];
        
        // Process the document content to extract unique words
        Set<String> uniqueWords = new HashSet<>();
        
        // Convert to lowercase and remove punctuation
        content = content.toLowerCase().replaceAll("[^a-zA-Z0-9\\s]", "");
        
        StringTokenizer tokenizer = new StringTokenizer(content);
        while (tokenizer.hasMoreTokens()) {
            String word = tokenizer.nextToken().trim();
            if (!word.isEmpty()) {
                uniqueWords.add(word);
            }
        }
        
        // Create a comma-separated string of unique words
        StringBuilder wordSetBuilder = new StringBuilder();
        boolean first = true;
        for (String word : uniqueWords) {
            if (!first) {
                wordSetBuilder.append(",");
            }
            wordSetBuilder.append(word);
            first = false;
        }
        
        documentId.set(docId);
        wordSet.set(wordSetBuilder.toString());
        
        context.write(documentId, wordSet);
    }
}