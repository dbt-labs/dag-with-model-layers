QUERY_LINEAGE = """
query Lineage($environmentId: BigInt!, $filter: AppliedResourcesFilter!) {
  environment(id: $environmentId) {
    applied {
      lineage(filter: $filter) {
        filePath
        uniqueId
        name
      }
    }
  }
}
"""
