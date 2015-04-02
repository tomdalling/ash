require 'ash/parser'

module Ash
  def self.parse(str)
    Parser.new.parse(str)
  end
end
