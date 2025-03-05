# Use the official Solr image
FROM solr:8.11.2

# Expose the Solr web interface port
EXPOSE 8983

# Start Solr when the container starts
CMD ["solr-foreground"]
