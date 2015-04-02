require 'parslet'

module Ash
  class Parser < Parslet::Parser
    rule(:ws) { match('\s').repeat(1) }
    rule(:ws?) { ws.maybe }

    rule(:ko) { str('ko') >> ws? }
    rule(:kun) { str('kun') >> ws? }

    rule(:word) { match('[a-z]').repeat(1) >> ws? }
    rule(:verb) { str('v') >> word }
    rule(:noun) { str('s') >> word }
    rule(:adjective) { str('l') >> word }

    rule(:noun1) { noun.as(:noun) >> adjective.repeat.as(:adjectives) }
    rule(:possessor) { ko >> noun1.as(:possessor) }
    rule(:noun_phrase) { noun1.as(:head) >> possessor.repeat.as(:possessors).maybe }

    rule(:verb_phrase) {
      verb.as(:verb) >> (noun_phrase.as(:object) >> (kun >> noun_phrase.as(:indirect_object)).maybe).maybe
    }

    rule(:clause) { noun_phrase.as(:subject) >> verb_phrase.as(:verb_phrase) }
    root(:clause)

    def parse(str)
      transform_ast(super(str))
    end

    private

      def transform_ast(ast)
        case ast
        when Parslet::Slice then ast.to_s.strip
        when String then ast.strip
        when Hash then Hash[ast.map { |key, child| [key, transform_ast(child)] }]
        when Array then ast.map { |child| transform_ast(child) }
        else raise StandardError, "Don't know how to walk this: #{ast.class.inspect}"
        end
      end

  end
end
